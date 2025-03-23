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
import sys

import cmd_arg
import config
import db
from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler
from media_platform.zhihu import ZhihuCrawler


class CrawlerFactory:
    """
    爬虫工厂类，用于根据不同的媒体平台创建相应的爬虫实例。
    """
    # 定义一个字典，将平台名称映射到对应的爬虫类
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler,
        "dy": DouYinCrawler,
        "ks": KuaishouCrawler,
        "bili": BilibiliCrawler,
        "wb": WeiboCrawler,
        "tieba": TieBaCrawler,
        "zhihu": ZhihuCrawler
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        """
        根据给定的平台名称创建相应的爬虫实例。

        :param platform: 媒体平台的名称，如 "xhs", "dy", "ks" 等。
        :return: 对应平台的爬虫实例，继承自 AbstractCrawler 类。
        :raises ValueError: 如果提供的平台名称无效，抛出此异常。
        """
        # 从 CRAWLERS 字典中获取对应平台的爬虫类
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        # 检查是否找到了对应的爬虫类
        if not crawler_class:
            # 如果未找到，抛出 ValueError 异常
            raise ValueError("Invalid Media Platform Currently only supported xhs or dy or ks or bili ...")
        # 创建并返回爬虫实例
        return crawler_class()


async def main():
    """
    主异步函数，用于协调整个爬虫程序的运行。
    包括解析命令行参数、初始化数据库、创建并启动爬虫，最后关闭数据库连接。
    """
    # parse cmd
    await cmd_arg.parse_cmd()  # 异步解析命令行参数

    # init db
    if config.SAVE_DATA_OPTION == "db":
        # 如果配置为将数据保存到数据库，则异步初始化数据库
        await db.init_db()

    # 使用CrawlerFactory根据配置中的平台创建相应的爬虫实例
    crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
    await crawler.start()  # 异步启动爬虫

    if config.SAVE_DATA_OPTION == "db":
        # 如果配置为将数据保存到数据库，则异步关闭数据库连接
        await db.close()


    

if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
