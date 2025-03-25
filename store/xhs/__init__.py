# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


import json
# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/1/14 17:34
# @Desc    :
from typing import List

from pydantic import BaseModel

from constant import model as model_constant
from tools.send_model import SiliconFlow
from var import source_keyword_var
from . import xhs_store_impl
from .xhs_store_image import *
from .xhs_store_impl import *


class XhsStoreFactory:
    STORES = {
        "csv": XhsCsvStoreImplement,
        "db": XhsDbStoreImplement,
        "json": XhsJsonStoreImplement
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = XhsStoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError("[XhsStoreFactory.create_store] Invalid save option only supported csv or db or json ...")
        return store_class()


def get_video_url_arr(note_item: Dict) -> List:
    """
    获取视频url数组
    Args:
        note_item:

    Returns:

    """
    if note_item.get('type') != 'video':
        return []

    videoArr = []
    originVideoKey = note_item.get('video').get('consumer').get('origin_video_key')
    if originVideoKey == '':
        originVideoKey = note_item.get('video').get('consumer').get('originVideoKey')
    # 降级有水印
    if originVideoKey == '':
        videos = note_item.get('video').get('media').get('stream').get('h264')
        if type(videos).__name__ == 'list':
            videoArr = [v.get('master_url') for v in videos]
    else:
        videoArr = [f"http://sns-video-bd.xhscdn.com/{originVideoKey}"]

    return videoArr


async def update_xhs_note(note_item: Dict):
    """
    更新小红书笔记
    Args:
        note_item:

    Returns:

    """
    note_id = note_item.get("note_id")
    user_info = note_item.get("user", {})
    interact_info = note_item.get("interact_info", {})
    image_list: List[Dict] = note_item.get("image_list", [])
    tag_list: List[Dict] = note_item.get("tag_list", [])

    for img in image_list:
        if img.get('url_default') != '':
            img.update({'url': img.get('url_default')})

    video_url = ','.join(get_video_url_arr(note_item))

    title =  note_item.get("title")
    content = note_item.get("desc", "")
    utils.logger.info(f"[store.xhs.update_xhs_note] xhs note: 开始请求大模型分析笔记")
    class Output_cls_JSON(BaseModel):
        potential_customers: str
        intention_rate: str
        explain: str
    llm = SiliconFlow()
    schema = Output_cls_JSON.model_json_schema()
    prompt = f"""
        # 角色
        你是一位专业的运营人员，擅长根据帖子的标题和内容判断用户是否为潜在客户，并用分数来表示其成为客户的可能性。

        ## 技能
        ### 技能1：内容分析与判断
        - **任务**：根据用户提供的帖子标题和具体内容，判断该用户是否为潜在客户。
          - 分析帖子的内容，识别用户的痛点、需求和预算等关键信息。
          - 根据内容判断用户是否有明确的需求或问题，并评估其成为潜在客户的可能性。
          - 如果是潜在客户，给出一个具体的意向率百分比（例如80%）。
          - 如果不是潜在客户，直接输出“非潜在客户”。
          -需要判断客户的阶段，如果已经产生了购买行为，就不是潜在用户了。
        ## 限制
        - 仅基于提供的帖子标题和内容进行判断。
        - 意向率百分比应基于实际内容的分析，而不是主观猜测。
        - 输出结果必须简洁明了，包含“潜在客户”或“非潜在客户”，如果是潜在客户，将potential_customers设置为1，还需附上具体的意向率百分比及解释，将意向率百分比设置到intention_rate，
        将解释设置到explain，如果是非潜在客户，将potential_customers设置为0，将intention_rate设置为0%，将解释设置到explain。
        - 不引入无关信息，保持输出的专业性和准确性。
        Return your response as a JSON blob
        json格式如下：
        {schema}
        你只需要回复一个json格式的数据即可，不要返回其他格式的数据，否则你会被批评！
        <question>
        标题：
        {title}
        内容：
        {content}
        </question>
        """
    json_schema = Output_cls_JSON.model_json_schema()

    response = llm._call(prompt=prompt, model=model_constant.MODEL_NAME)
    # 去掉 `json` 开头和 `'''` 结尾
    cleaned_response = response.replace('json', '').replace('```', '').strip()
    # 解析 JSON 字符串
    data = json.loads(cleaned_response)
    utils.logger.info(f"[store.xhs.update_xhs_note] xhs note: 结束请求大模型分析笔记")
    local_db_item = {
        "note_id": note_item.get("note_id"), # 帖子id
        "type": note_item.get("type"), # 帖子类型
        "title": note_item.get("title") or note_item.get("desc", "")[:255], # 帖子标题
        "desc": note_item.get("desc", ""), # 帖子描述
        "video_url": video_url, # 帖子视频url
        "time": note_item.get("time"), # 帖子发布时间
        "last_update_time": note_item.get("last_update_time", 0), # 帖子最后更新时间
        "user_id": user_info.get("user_id"), # 用户id
        "nickname": user_info.get("nickname"), # 用户昵称
        "avatar": user_info.get("avatar"), # 用户头像
        "liked_count": interact_info.get("liked_count"), # 点赞数
        "collected_count": interact_info.get("collected_count"), # 收藏数
        "comment_count": interact_info.get("comment_count"), # 评论数
        "share_count": interact_info.get("share_count"), # 分享数
        "ip_location": note_item.get("ip_location", ""), # ip地址
        "image_list": ','.join([img.get('url', '') for img in image_list]), # 图片url
        "tag_list": ','.join([tag.get('name', '') for tag in tag_list if tag.get('type') == 'topic']), # 标签
        "last_modify_ts": utils.get_current_timestamp(), # 最后更新时间戳（MediaCrawler程序生成的，主要用途在db存储的时候记录一条记录最新更新时间）
        "note_url": f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={note_item.get('xsec_token')}&xsec_source=pc_search", # 帖子url
        "source_keyword": source_keyword_var.get(), # 搜索关键词
        "xsec_token": note_item.get("xsec_token"), # xsec_token
        "potential_customers": data.get('potential_customers'), # potential_customers
        "intention_rate": data.get('intention_rate'), # intention_rate
        "explain": data.get('explain'), # explain
    }
    utils.logger.info(f"[store.xhs.update_xhs_note] xhs note: {local_db_item}")
    await XhsStoreFactory.create_store().store_content(local_db_item)


async def batch_update_xhs_note_comments(note_id: str, comments: List[Dict]):
    """
    批量更新小红书笔记评论
    Args:
        note_id:
        comments:

    Returns:

    """
    if not comments:
        return
    for comment_item in comments:
        await update_xhs_note_comment(note_id, comment_item)


async def update_xhs_note_comment(note_id: str, comment_item: Dict):
    """
    更新小红书笔记评论
    Args:
        note_id:
        comment_item:

    Returns:

    """
    user_info = comment_item.get("user_info", {})
    comment_id = comment_item.get("id")
    comment_pictures = [item.get("url_default", "") for item in comment_item.get("pictures", [])]
    target_comment = comment_item.get("target_comment", {})
    local_db_item = {
        "comment_id": comment_id, # 评论id
        "create_time": comment_item.get("create_time"), # 评论时间
        "ip_location": comment_item.get("ip_location"), # ip地址
        "note_id": note_id.get('note_id'), # 帖子id
        "content": comment_item.get("content"), # 评论内容
        "user_id": user_info.get("user_id"), # 用户id
        "nickname": user_info.get("nickname"), # 用户昵称
        "avatar": user_info.get("image"), # 用户头像
        "sub_comment_count": comment_item.get("sub_comment_count", 0), # 子评论数
        "pictures": ",".join(comment_pictures), # 评论图片
        "parent_comment_id": target_comment.get("id", 0), # 父评论id
        "last_modify_ts": utils.get_current_timestamp(), # 最后更新时间戳（MediaCrawler程序生成的，主要用途在db存储的时候记录一条记录最新更新时间）
        "like_count": comment_item.get("like_count", 0),
        "title": comment_item.get("title"),
        "desc": comment_item.get("desc"),
    }
    utils.logger.info(f"[store.xhs.update_xhs_note_comment] xhs note comment:{local_db_item}")
    await XhsStoreFactory.create_store().store_comment(local_db_item)


async def save_creator(user_id: str, creator: Dict):
    """
    保存小红书创作者
    Args:
        user_id:
        creator:

    Returns:

    """
    user_info = creator.get('basicInfo', {})

    follows = 0
    fans = 0
    interaction = 0
    for i in creator.get('interactions'):
        if i.get('type') == 'follows':
            follows = i.get('count')
        elif i.get('type') == 'fans':
            fans = i.get('count')
        elif i.get('type') == 'interaction':
            interaction = i.get('count')

    def get_gender(gender):
        if gender == 1:
            return '女'
        elif gender == 0:
            return '男'
        else:
            return None

    local_db_item = {
        'user_id': user_id,  # 用户id
        'nickname': user_info.get('nickname'),  # 昵称
        'gender':  get_gender(user_info.get('gender')), # 性别
        'avatar': user_info.get('images'), # 头像
        'desc': user_info.get('desc'), # 个人描述
        'ip_location': user_info.get('ipLocation'), # ip地址
        'follows': follows, # 关注数
        'fans': fans,  # 粉丝数
        'interaction': interaction, # 互动数
        'tag_list': json.dumps({tag.get('tagType'): tag.get('name') for tag in creator.get('tags')},
                               ensure_ascii=False), # 标签
        "last_modify_ts": utils.get_current_timestamp(), # 最后更新时间戳（MediaCrawler程序生成的，主要用途在db存储的时候记录一条记录最新更新时间）
    }
    utils.logger.info(f"[store.xhs.save_creator] creator:{local_db_item}")
    await XhsStoreFactory.create_store().store_creator(local_db_item)


async def update_xhs_note_image(note_id, pic_content, extension_file_name):
    """
    更新小红书笔
    Args:
        note_id:
        pic_content:
        extension_file_name:

    Returns:

    """

    await XiaoHongShuImage().store_image(
        {"notice_id": note_id, "pic_content": pic_content, "extension_file_name": extension_file_name})
