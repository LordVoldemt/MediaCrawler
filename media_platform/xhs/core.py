# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。


import asyncio
import os
import random
import time
from asyncio import Task
from typing import Dict, List, Optional, Tuple

from playwright.async_api import BrowserContext, BrowserType, Page, async_playwright
from tenacity import RetryError

import config
from base.base_crawler import AbstractCrawler
from config import CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES
from model.m_xiaohongshu import NoteUrlInfo
from proxy.proxy_ip_pool import IpInfoModel, create_ip_pool
from store import xhs as xhs_store
from tools import utils
from var import crawler_type_var, source_keyword_var

from .client import XiaoHongShuClient
from .exception import DataFetchError
from .field import SearchSortType
from .help import parse_note_info_from_note_url, get_search_id
from .login import XiaoHongShuLogin
from pydantic import BaseModel

from tools.send_model import SiliconFlow
import json
from constant import model as model_constant

class XiaoHongShuCrawler(AbstractCrawler):
    # 定义浏览器上下文页面
    context_page: Page
    # 定义小红书客户端实例
    xhs_client: XiaoHongShuClient
    # 定义浏览器上下文
    browser_context: BrowserContext

    def __init__(self) -> None:
        # 初始化小红书首页URL
        self.index_url = "https://www.xiaohongshu.com"
        # 如果配置文件中有指定User-Agent，则使用配置中的，否则使用默认值
        # self.user_agent = utils.get_user_agent()
        self.user_agent = config.UA if config.UA else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

    async def start(self) -> None:
        # 初始化Playwright和Httpx使用的代理格式
        playwright_proxy_format, httpx_proxy_format = None, None
        # 如果启用了IP代理
        if config.ENABLE_IP_PROXY:
            # 创建IP代理池
            ip_proxy_pool = await create_ip_pool(
                config.IP_PROXY_POOL_COUNT, enable_validate_ip=True
            )
            # 从代理池中获取一个代理
            ip_proxy_info: IpInfoModel = await ip_proxy_pool.get_proxy()
            # 格式化代理信息，供Playwright和Httpx使用
            playwright_proxy_format, httpx_proxy_format = self.format_proxy_info(
                ip_proxy_info
            )

        # 异步启动Playwright
        async with async_playwright() as playwright:
            # 获取Chromium浏览器类型
            chromium = playwright.chromium
            # 启动浏览器上下文
            self.browser_context = await self.launch_browser(
                chromium, None, self.user_agent, headless=config.HEADLESS
            )
            # 注入stealth.min.js脚本，防止网站检测到爬虫
            await self.browser_context.add_init_script(path="libs/stealth.min.js")
            # 添加cookie，避免网页出现滑动验证码
            await self.browser_context.add_cookies(
                [
                    {
                        "name": "webId",
                        "value": "xxx123",  # 任意值
                        "domain": ".xiaohongshu.com",
                        "path": "/",
                    }
                ]
            )
            # 创建一个新页面
            self.context_page = await self.browser_context.new_page()
            # 访问小红书首页
            await self.context_page.goto(self.index_url)

            # 创建小红书客户端实例
            self.xhs_client = await self.create_xhs_client(httpx_proxy_format)
            # 检查客户端是否可以正常连接
            if not await self.xhs_client.pong():
                # 如果无法连接，进行登录操作
                login_obj = XiaoHongShuLogin(
                    login_type=config.LOGIN_TYPE,
                    login_phone="",  # 输入你的手机号码
                    browser_context=self.browser_context,
                    context_page=self.context_page,
                    cookie_str=config.COOKIES,
                )
                await login_obj.begin()
                # 更新客户端的cookie
                await self.xhs_client.update_cookies(
                    browser_context=self.browser_context
                )

            # 设置爬虫类型
            crawler_type_var.set(config.CRAWLER_TYPE)
            # 根据配置的爬虫类型执行不同的操作
            if config.CRAWLER_TYPE == "search":
                # 搜索笔记并获取评论信息
                await self.search()
            elif config.CRAWLER_TYPE == "detail":
                # 获取指定帖子的信息和评论
                await self.get_specified_notes()
            elif config.CRAWLER_TYPE == "creator":
                # 获取创作者的信息、笔记和评论
                await self.get_creators_and_notes()
            else:
                pass

            # 记录日志，表示小红书爬虫完成
            utils.logger.info("[XiaoHongShuCrawler.start] Xhs Crawler finished ...")

    async def search(self) -> None:
        """
        搜索笔记并获取其评论信息。
        """
        # 记录日志，表示开始搜索小红书关键词
        utils.logger.info(
            "[XiaoHongShuCrawler.search] Begin search xiaohongshu keywords"
        )
        # 小红书每页固定返回的笔记数量
        xhs_limit_count = 20
        # 如果配置的最大笔记数量小于小红书每页固定数量，将其设置为固定数量
        if config.CRAWLER_MAX_NOTES_COUNT < xhs_limit_count:
            config.CRAWLER_MAX_NOTES_COUNT = xhs_limit_count
        # 获取起始页码
        start_page = config.START_PAGE
        # 遍历配置中的关键词列表
        for keyword in config.KEYWORDS.split(","):
            # 设置当前搜索的关键词
            source_keyword_var.set(keyword)
            # 记录日志，表示当前搜索的关键词
            utils.logger.info(
                f"[XiaoHongShuCrawler.search] Current search keyword: {keyword}"
            )
            # 初始化页码为1
            page = 1
            # 获取搜索ID
            search_id = get_search_id()
            # 循环搜索，直到达到最大笔记数量
            while (
                page - start_page + 1
            ) * xhs_limit_count <= config.CRAWLER_MAX_NOTES_COUNT:
                # 如果当前页码小于起始页码，跳过该页
                if page < start_page:
                    utils.logger.info(f"[XiaoHongShuCrawler.search] Skip page {page}")
                    page += 1
                    continue

                try:
                    # 记录日志，表示正在搜索指定关键词和页码的笔记
                    utils.logger.info(
                        f"[XiaoHongShuCrawler.search] search xhs keyword: {keyword}, page: {page}"
                    )
                    # 初始化笔记ID列表
                    note_ids: List[str] = []
                    # 初始化xsec_token列表
                    xsec_tokens: List[str] = []
                    # 通过关键词搜索笔记
                    notes_res = await self.xhs_client.get_note_by_keyword(
                        keyword=keyword,
                        search_id=search_id,
                        page=page,
                        sort=(
                            SearchSortType(config.SORT_TYPE)
                            if config.SORT_TYPE != ""
                            else SearchSortType.GENERAL
                        ),
                    )
                    # 记录日志，表示搜索笔记的结果
                    utils.logger.info(
                        f"[XiaoHongShuCrawler.search] Search notes res:{notes_res}"
                    )
                    # 如果没有搜索结果或没有更多内容，跳出循环
                    if not notes_res or not notes_res.get("has_more", False):
                        utils.logger.info("No more content!")
                        break
                    # 创建异步信号量，控制并发数量
                    semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
                    # 创建异步任务列表，获取笔记详情
                    task_list = [
                        self.get_note_detail_async_task(
                            note_id=post_item.get("id"),
                            xsec_source=post_item.get("xsec_source"),
                            xsec_token=post_item.get("xsec_token"),
                            semaphore=semaphore,
                        )
                        for post_item in notes_res.get("items", {})
                        if post_item.get("model_type") not in ("rec_query", "hot_query")
                    ]
                    # 并发执行任务，获取笔记详情
                    note_details = await asyncio.gather(*task_list)
                    # 遍历笔记详情列表
                    for note_detail in note_details:
                        if note_detail:
                            # 更新笔记信息到数据库
                            await xhs_store.update_xhs_note(note_detail)
                            # 获取笔记的媒体信息
                            await self.get_notice_media(note_detail)
                            # 将笔记ID添加到列表中
                            note_ids.append(note_detail.get("note_id"))
                            # 将xsec_token添加到列表中
                            xsec_tokens.append(note_detail.get("xsec_token"))
                    # 页码加1
                    page += 1
                    # 记录日志，表示笔记详情信息
                    utils.logger.info(
                        f"[XiaoHongShuCrawler.search] Note details: {note_details}"
                    )
                    # 批量获取笔记的评论信息
                    await self.batch_get_note_comments(note_ids, xsec_tokens)
                except DataFetchError:
                    # 记录日志，表示获取笔记详情时出错
                    utils.logger.error(
                        "[XiaoHongShuCrawler.search] Get note detail error"
                    )
                    break

    async def get_creators_and_notes(self) -> None:
        """
        获取创作者的笔记并获取其评论信息。
        """
        # 记录日志，表示开始获取小红书创作者信息
        utils.logger.info(
            "[XiaoHongShuCrawler.get_creators_and_notes] Begin get xiaohongshu creators"
        )
        # 遍历配置中的创作者ID列表
        for user_id in config.XHS_CREATOR_ID_LIST:
            # 从网页HTML内容中获取创作者的详细信息
            createor_info: Dict = await self.xhs_client.get_creator_info(
                user_id=user_id
            )
            if createor_info:
                # 将创作者信息保存到数据库
                await xhs_store.save_creator(user_id, creator=createor_info)

            # 如果未启用代理，增加爬取间隔
            if config.ENABLE_IP_PROXY:
                crawl_interval = random.random()
            else:
                crawl_interval = random.uniform(1, config.CRAWLER_MAX_SLEEP_SEC)
            # 获取创作者的所有笔记信息
            all_notes_list = await self.xhs_client.get_all_notes_by_creator(
                user_id=user_id,
                crawl_interval=crawl_interval,
                callback=self.fetch_creator_notes_detail,
            )

            # 初始化笔记ID列表
            note_ids = []
            # 初始化xsec_token列表
            xsec_tokens = []
            # 遍历笔记列表
            for note_item in all_notes_list:
                # 将笔记ID添加到列表中
                note_ids.append(note_item.get("note_id"))
                # 将xsec_token添加到列表中
                xsec_tokens.append(note_item.get("xsec_token"))
            # 批量获取笔记的评论信息
            await self.batch_get_note_comments(note_ids, xsec_tokens)

    async def fetch_creator_notes_detail(self, note_list: List[Dict]):
        """
        并发获取指定帖子列表并保存数据
        """
        # 创建异步信号量，控制并发数量
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        # 创建异步任务列表，获取笔记详情
        task_list = [
            self.get_note_detail_async_task(
                note_id=post_item.get("note_id"),
                xsec_source=post_item.get("xsec_source"),
                xsec_token=post_item.get("xsec_token"),
                semaphore=semaphore,
            )
            for post_item in note_list
        ]

        # 并发执行任务，获取笔记详情
        note_details = await asyncio.gather(*task_list)
        # 遍历笔记详情列表
        for note_detail in note_details:
            if note_detail:
                # 更新笔记信息到数据库
                await xhs_store.update_xhs_note(note_detail)

    async def get_specified_notes(self):
        """
        获取指定帖子的信息和评论
        必须指定note_id, xsec_source, xsec_token⚠️⚠️⚠️
        Returns:

        """
        # 初始化获取笔记详情的任务列表
        get_note_detail_task_list = []
        # 遍历配置中的指定笔记URL列表
        for full_note_url in config.XHS_SPECIFIED_NOTE_URL_LIST:
            # 解析笔记URL信息
            note_url_info: NoteUrlInfo = parse_note_info_from_note_url(full_note_url)
            # 记录日志，表示解析笔记URL信息
            utils.logger.info(
                f"[XiaoHongShuCrawler.get_specified_notes] Parse note url info: {note_url_info}"
            )
            # 创建异步任务，获取笔记详情
            crawler_task = self.get_note_detail_async_task(
                note_id=note_url_info.note_id,
                xsec_source=note_url_info.xsec_source,
                xsec_token=note_url_info.xsec_token,
                semaphore=asyncio.Semaphore(config.MAX_CONCURRENCY_NUM),
            )
            # 将任务添加到任务列表中
            get_note_detail_task_list.append(crawler_task)

        # 初始化需要获取评论的笔记ID列表
        need_get_comment_note_ids = []
        # 初始化xsec_token列表
        xsec_tokens = []
        # 并发执行任务，获取笔记详情
        note_details = await asyncio.gather(*get_note_detail_task_list)
        # 遍历笔记详情列表
        for note_detail in note_details:
            if note_detail:
                # 将笔记ID添加到需要获取评论的列表中
                need_get_comment_note_ids.append(note_detail.get("note_id", ""))
                # 将xsec_token添加到列表中
                xsec_tokens.append(note_detail.get("xsec_token", ""))
                # 更新笔记信息到数据库
                await xhs_store.update_xhs_note(note_detail)
        # 批量获取笔记的评论信息
        await self.batch_get_note_comments(need_get_comment_note_ids, xsec_tokens)

    async def get_note_detail_async_task(
        self,
        note_id: str,
        xsec_source: str,
        xsec_token: str,
        semaphore: asyncio.Semaphore,
    ) -> Optional[Dict]:
        """
        获取笔记详情

        Args:
            note_id: 笔记ID
            xsec_source: xsec_source参数
            xsec_token: xsec_token参数
            semaphore: 异步信号量，用于控制并发

        Returns:
            Dict: 笔记详情，如果获取失败则返回None
        """
        # 初始化从HTML和API获取的笔记详情
        note_detail_from_html, note_detail_from_api = None, None
        # 使用异步信号量控制并发
        async with semaphore:
            # 如果未启用代理，增加爬取间隔
            if config.ENABLE_IP_PROXY:
                crawl_interval = random.random()
            else:
                crawl_interval = random.uniform(1, config.CRAWLER_MAX_SLEEP_SEC)
            try:
                # 尝试直接获取网页版笔记详情，携带cookie
                note_detail_from_html: Optional[Dict] = (
                    await self.xhs_client.get_note_by_id_from_html(
                        note_id, xsec_source, xsec_token, enable_cookie=True
                    )
                )
                # 等待爬取间隔时间
                time.sleep(crawl_interval)
                if not note_detail_from_html:
                    # 如果网页版笔记详情获取失败，则尝试不使用cookie获取
                    note_detail_from_html = (
                        await self.xhs_client.get_note_by_id_from_html(
                            note_id, xsec_source, xsec_token, enable_cookie=False
                        )
                    )
                    # 记录日志，表示获取笔记详情失败
                    utils.logger.error(
                        f"[XiaoHongShuCrawler.get_note_detail_async_task] Get note detail error, note_id: {note_id}"
                    )
                if not note_detail_from_html:
                    # 如果网页版笔记详情获取失败，则尝试API获取
                    note_detail_from_api: Optional[Dict] = (
                        await self.xhs_client.get_note_by_id(
                            note_id, xsec_source, xsec_token
                        )
                    )
                # 优先使用从HTML获取的笔记详情，否则使用API获取的
                note_detail = note_detail_from_html or note_detail_from_api
                if note_detail:
                    # 更新笔记详情中的xsec_token和xsec_source
                    note_detail.update(
                        {"xsec_token": xsec_token, "xsec_source": xsec_source}
                    )
                    return note_detail
            except DataFetchError as ex:
                # 记录日志，表示获取笔记详情时出现数据获取错误
                utils.logger.error(
                    f"[XiaoHongShuCrawler.get_note_detail_async_task] Get note detail error: {ex}"
                )
                return None
            except KeyError as ex:
                # 记录日志，表示未找到笔记详情
                utils.logger.error(
                    f"[XiaoHongShuCrawler.get_note_detail_async_task] have not fund note detail note_id:{note_id}, err: {ex}"
                )
                return None

    async def batch_get_note_comments(
        self, note_list: List[str], xsec_tokens: List[str]
    ):
        """
        批量获取笔记的评论信息
        """
        # 如果未启用获取评论功能，记录日志并返回
        if not config.ENABLE_GET_COMMENTS:
            utils.logger.info(
                f"[XiaoHongShuCrawler.batch_get_note_comments] Crawling comment mode is not enabled"
            )
            return

        # 记录日志，表示开始批量获取笔记的评论信息
        utils.logger.info(
            f"[XiaoHongShuCrawler.batch_get_note_comments] Begin batch get note comments, note list: {note_list}"
        )
        # 创建异步信号量，控制并发数量
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        # 初始化任务列表
        task_list: List[Task] = []
        # 遍历笔记ID列表
        for index, note_id in enumerate(note_list):
            # 创建异步任务，获取笔记的评论信息
            task = asyncio.create_task(
                self.get_comments(
                    note_id=note_id, xsec_token=xsec_tokens[index], semaphore=semaphore
                ),
                name=note_id,
            )
            # 将任务添加到任务列表中
            task_list.append(task)
        # 并发执行任务，获取笔记的评论信息
        await asyncio.gather(*task_list)

    async def get_comments(
        self, note_id: str, xsec_token: str, semaphore: asyncio.Semaphore
    ):
        """
        获取笔记的评论信息，并进行关键词过滤和数量限制
        """
        # 使用异步信号量控制并发
        async with semaphore:
            # 记录日志，表示开始获取指定笔记的评论信息
            utils.logger.info(
                f"[XiaoHongShuCrawler.get_comments] Begin get note id comments {note_id}"
            )
            # 如果未启用代理，增加爬取间隔
            if config.ENABLE_IP_PROXY:
                crawl_interval = random.random()
            else:
                crawl_interval = random.uniform(1, config.CRAWLER_MAX_SLEEP_SEC)
            # 获取笔记的所有评论信息
            await self.xhs_client.get_note_all_comments(
                note_id=note_id,
                xsec_token=xsec_token,
                crawl_interval=crawl_interval,
                callback=xhs_store.batch_update_xhs_note_comments,
                max_count=CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES,
            )

    @staticmethod
    def format_proxy_info(
        ip_proxy_info: IpInfoModel,
    ) -> Tuple[Optional[Dict], Optional[Dict]]:
        """
        格式化代理信息，供Playwright和Httpx使用

        Args:
            ip_proxy_info: IP代理信息模型

        Returns:
            Tuple[Optional[Dict], Optional[Dict]]: 格式化后的Playwright和Httpx代理信息
        """
        # 格式化Playwright使用的代理信息
        playwright_proxy = {
            "server": f"{ip_proxy_info.protocol}{ip_proxy_info.ip}:{ip_proxy_info.port}",
            "username": ip_proxy_info.user,
            "password": ip_proxy_info.password,
        }
        # 格式化Httpx使用的代理信息
        httpx_proxy = {
            f"{ip_proxy_info.protocol}": f"http://{ip_proxy_info.user}:{ip_proxy_info.password}@{ip_proxy_info.ip}:{ip_proxy_info.port}"
        }
        return playwright_proxy, httpx_proxy

    async def create_xhs_client(self, httpx_proxy: Optional[str]) -> XiaoHongShuClient:
        """
        创建小红书客户端实例

        Args:
            httpx_proxy: Httpx使用的代理信息

        Returns:
            XiaoHongShuClient: 小红书客户端实例
        """
        # 记录日志，表示开始创建小红书API客户端
        utils.logger.info(
            "[XiaoHongShuCrawler.create_xhs_client] Begin create xiaohongshu API client ..."
        )
        # 转换浏览器上下文中的cookie为字符串和字典形式
        cookie_str, cookie_dict = utils.convert_cookies(
            await self.browser_context.cookies()
        )
        # 创建小红书客户端实例
        xhs_client_obj = XiaoHongShuClient(
            proxies=httpx_proxy,
            headers={
                "User-Agent": self.user_agent,
                "Cookie": cookie_str,
                "Origin": "https://www.xiaohongshu.com",
                "Referer": "https://www.xiaohongshu.com",
                "Content-Type": "application/json;charset=UTF-8",
            },
            playwright_page=self.context_page,
            cookie_dict=cookie_dict,
        )
        return xhs_client_obj

    async def launch_browser(
        self,
        chromium: BrowserType,
        playwright_proxy: Optional[Dict],
        user_agent: Optional[str],
        headless: bool = True,
    ) -> BrowserContext:
        """
        启动浏览器并创建浏览器上下文

        Args:
            chromium: 浏览器类型（Chromium）
            playwright_proxy: Playwright使用的代理信息
            user_agent: 用户代理
            headless: 是否无头模式，默认为True

        Returns:
            BrowserContext: 浏览器上下文
        """
        # 记录日志，表示开始创建浏览器上下文
        utils.logger.info(
            "[XiaoHongShuCrawler.launch_browser] Begin create browser context ..."
        )
        # 如果配置了保存登录状态
        if config.SAVE_LOGIN_STATE:
            # 保存登录状态，避免每次都登录
            user_data_dir = os.path.join(
                os.getcwd(), "browser_data", config.USER_DATA_DIR % config.PLATFORM
            )  # type: ignore
            # 启动持久化浏览器上下文
            browser_context = await chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                accept_downloads=True,
                headless=headless,
                proxy=playwright_proxy,  # type: ignore
                viewport={"width": 1920, "height": 1080},
                user_agent=user_agent,
            )
            return browser_context
        else:
            # 启动普通浏览器
            browser = await chromium.launch(headless=headless, proxy=playwright_proxy)  # type: ignore
            # 创建新的浏览器上下文
            browser_context = await browser.new_context(
                viewport={"width": 1920, "height": 1080}, user_agent=user_agent
            )
            return browser_context

    async def close(self):
        """
        关闭浏览器上下文
        """
        # 关闭浏览器上下文
        await self.browser_context.close()
        # 记录日志，表示浏览器上下文已关闭
        utils.logger.info("[XiaoHongShuCrawler.close] Browser context closed ...")

    async def get_notice_media(self, note_detail: Dict):
        """
        获取笔记的媒体信息（图片和视频）

        Args:
            note_detail: 笔记详情字典
        """
        # 如果未启用获取图片功能，记录日志并返回
        if not config.ENABLE_GET_IMAGES:
            utils.logger.info(
                f"[XiaoHongShuCrawler.get_notice_media] Crawling image mode is not enabled"
            )
            return
        # 获取笔记的图片信息
        await self.get_note_images(note_detail)
        # 获取笔记的视频信息
        await self.get_notice_video(note_detail)

    async def get_note_images(self, note_item: Dict):
        """
        获取笔记的图片信息。请使用 get_notice_media 方法

        Args:
            note_item: 笔记信息字典

        Returns:
            None
        """
        # 如果未启用获取图片功能，直接返回
        if not config.ENABLE_GET_IMAGES:
            return
        # 获取笔记ID
        note_id = note_item.get("note_id")
        # 获取笔记的图片列表
        image_list: List[Dict] = note_item.get("image_list", [])

        # 遍历图片列表，更新图片URL
        for img in image_list:
            if img.get("url_default") != "":
                img.update({"url": img.get("url_default")})

        # 如果图片列表为空，直接返回
        if not image_list:
            return
        # 初始化图片编号
        picNum = 0
        # 遍历图片列表
        for pic in image_list:
            # 获取图片URL
            url = pic.get("url")
            if not url:
                continue
            # 获取图片内容
            content = await self.xhs_client.get_note_media(url)
            if content is None:
                continue
            # 生成图片文件名
            extension_file_name = f"{picNum}.jpg"
            # 图片编号加1
            picNum += 1
            # 更新笔记图片信息到数据库
            await xhs_store.update_xhs_note_image(note_id, content, extension_file_name)

    async def get_notice_video(self, note_item: Dict):
        """
        获取笔记的视频信息。请使用 get_notice_media 方法

        Args:
            note_item: 笔记信息字典

        Returns:
            None
        """
        # 如果未启用获取图片功能，直接返回
        if not config.ENABLE_GET_IMAGES:
            return
        # 获取笔记ID
        note_id = note_item.get("note_id")

        # 获取笔记的视频URL列表
        videos = xhs_store.get_video_url_arr(note_item)

        # 如果视频列表为空，直接返回
        if not videos:
            return
        # 初始化视频编号
        videoNum = 0
        # 遍历视频URL列表
        for url in videos:
            # 获取视频内容
            content = await self.xhs_client.get_note_media(url)
            if content is None:
                continue
            # 生成视频文件名
            extension_file_name = f"{videoNum}.mp4"
            # 视频编号加1
            videoNum += 1
            # 更新笔记视频信息到数据库
            await xhs_store.update_xhs_note_image(note_id, content, extension_file_name)
