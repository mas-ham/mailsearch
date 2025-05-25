"""
メール検索用モデル

create 2025/05/24 hamada
"""
import dataclasses

@dataclasses.dataclass
class MailSearchModel:
    search_val: str = ''
    search_val_list: list = None
    search_type: str = '01'
    is_target_title: bool = True
    is_target_body: bool = True
    search_from_date: str = ''
    search_to_date: str = ''
    is_target_receive: bool = True
    is_target_send: bool = True
    to_list: list = None
    sender_list: list = None
    folder_list: list = None

@dataclasses.dataclass
class SlackDetailModel:
    channel_type: str = ''
    channel_name: str = ''
    post_date: str = ''
    search_val: str = ''
    search_val_list: list = None

@dataclasses.dataclass
class SlackResultModel:
    post_date: str = ''
    post_icon: str = ''
    post_name: str = ''
    post_message: str = ''
    result_list: list = None
