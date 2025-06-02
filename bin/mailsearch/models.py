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
    sender_input_list: list = None
    to_list: list = None
    sender_list: list = None
    folder_list: list = None
    sent_folder_list: list = None

@dataclasses.dataclass
class MailDetailModel:
    entry_id: str = ''
    store_id: str = ''
    search_val: str = ''
    search_val_list: list = None

@dataclasses.dataclass
class MailResultModel:
    entry_id: str = ''
    store_id: str = ''
    folder_path: str = ''
    received: str = ''
    sender: str = ''
    sender_name: str = ''
    to_email: str = ''
    cc_email: str = ''
    subject: str = ''
    body: str = ''
