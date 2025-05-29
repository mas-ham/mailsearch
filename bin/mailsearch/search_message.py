"""
メールから検索する

create 2025/05/24 hamada
"""
import os
import re

import pythoncom
import win32com.client
import dateutil
import pandas as pd
import bleach

from common import const, sql_shared_service
from mailsearch.models import MailSearchModel, SlackDetailModel, SlackResultModel
from dataaccess.ext.search_dataaccess import SearchDataaccess
from dataaccess.general.target_sender_dataaccess import TargetSenderDataAccess
from dataaccess.general.target_folder_dataaccess import TargetFolderDataAccess
from dataaccess.common.set_cond_model import Condition
from dataaccess.common.set_sort_model import OrderBy
from dataaccess.general.tr_mail_messages_dataaccess import TrMailMessagesDataAccess



def get_sender_list(conn):

    dataaccess = TargetSenderDataAccess(conn)
    cond = [
        Condition('is_display', 1)
    ]
    results = dataaccess.select(conditions=cond)

    sender_list = []
    for sender in results:
        sender_list.append({
            'sender_id': sender.sender_id,
            'email_address': sender.email_address,
            'display_name': sender.display_name,
            'is_display': sender.is_display,
            'is_checked': sender.is_checked,
        })

    return sender_list


def get_folder_list(conn):

    dataaccess = TargetFolderDataAccess(conn)
    cond = [
        Condition('is_target', 1)
    ]
    sort = [
        OrderBy('folder_path')
    ]
    results = dataaccess.select(conditions=cond, order_by_list=sort)

    folder_list = []
    for folder in results:
        folder_list.append({
            'folder_id': folder.folder_id,
            'folder_path': folder.folder_path.split('\\')[-1],
            'is_target': folder.is_target,
        })

    return folder_list


def search(conn, root_dir, model: MailSearchModel):
    """
    検索

    Args:
        conn:
        root_dir:
        model:

    Returns:

    """

    # FIXME:
    dataaccess = SearchDataaccess(conn)
    results = dataaccess.search(model)

    result_list = []
    for _, row in results.iterrows():
        result_list.append({
            'folder_path': row['folder_path'],
            'sender': row['sender'],
            'sender_name': row['sender_name'],
            'received': row['received'],
            'subject': row['subject'],
        })
    return result_list

    # pythoncom.CoInitialize() # type: ignore
    # outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    # inbox = outlook.GetDefaultFolder(6)
    #
    # results = []
    #
    # def match_keywords(text):
    #     if not text:
    #         return False
    #     if not model.search_val_list:
    #         return True
    #     if model.search_type == '01':
    #         return all(kw.lower() in text.lower() for kw in model.search_val_list)
    #     else:
    #         return any(kw.lower() in text.lower() for kw in model.search_val_list)
    #
    # def is_within_date_range(mail):
    #     if not model.search_from_date and not model.search_to_date:
    #         return True
    #     mail_time = mail.ReceivedTime
    #     start_date = dateutil.parser.parse(model.search_from_date) if model.search_from_date else ''
    #     end_date = dateutil.parser.parse(model.search_to_date) if model.search_to_date else ''
    #     return ((not start_date or mail_time >= start_date) and
    #             (not end_date or mail_time <= end_date))
    #
    # def is_sender_match(mail):
    #     if not model.sender_list:
    #         return True
    #     sender = str(mail.SenderEmailAddress).lower()
    #     return any(addr.lower() in sender for addr in model.sender_list)
    #
    # # def is_to_match(mail):
    # #     if not model.to_list:
    # #         return True
    # #     sender = str(mail.SenderEmailAddress).lower()
    # #     return any(addr.lower() in sender for addr in model.to_list)
    #
    # def match_mail(mail):
    #     try:
    #         if mail.Class != 43:
    #             return False
    #         if model.is_target_title and not model.is_target_body:
    #             target_text = mail.Subject
    #         elif model.is_target_body and not model.is_target_title:
    #             target_text = mail.Body
    #         else:
    #             target_text = (mail.Subject or "") + " " + (mail.Body or "")
    #
    #         return (match_keywords(target_text)
    #                 and is_within_date_range(mail)
    #                 and is_sender_match(mail))
    #     except:
    #         return False
    #
    # def search_folder(folder, folder_path=""):
    #     current_path = f"{folder_path}\\{folder.Name}" if folder_path else folder.Name
    #     try:
    #         for mail in folder.Items:
    #             if match_mail(mail):
    #                 results.append({
    #                     "subject": mail.Subject,
    #                     "sender": mail.SenderEmailAddress,
    #                     "received": mail.ReceivedTime,
    #                     "entry_id": mail.EntryID,
    #                     "folder_path": current_path
    #                 })
    #     except Exception as e:
    #         pass  # アイテムアクセス不可でも無視
    #
    #     for subfolder in folder.Folders:
    #         search_folder(subfolder, current_path)
    #
    #
    # # 開始：受信トレイから再帰的に検索
    # search_folder(inbox)
    #
    # return results


def _convert_to_json_for_search(record_list, search_val_list):
    """
    検索結果画面に返却する用にJSONへコンバート
    Args:
        record_list:

    Returns:

    """
    if record_list.empty:
        return []

    result_list = []
    before_key = ''
    for _, row in record_list.iterrows():
        if before_key == row['post_date']:
            continue

        result_list.append({
            'channel_name': row['channel_name'],
            'post_name': row['post_name'],
            'post_date': row['post_date'],
            'post_message': _add_highlights(row['post_message'], search_val_list),
            'channel_type': row['channel_type'],
        })

        before_key = row['post_date']

    return result_list


def get_detail(root_dir, model: SlackDetailModel) -> SlackResultModel:
    """
    詳細を取得

    Args:
        root_dir:
        model:

    Returns:

    """
    result = SlackResultModel()
    result.post_date = model.post_date
    df = pd.read_excel(os.path.join(root_dir, const.EXPORT_DIR, model.channel_type, f'{model.channel_name}.xlsx'), dtype=str).fillna('').query('post_date == "' + result.post_date + '"')

    result_list = []
    for _, row in df.iterrows():
        if not result.post_name:
            result.post_name = row['post_name']
            result.post_message = _add_highlights(row['post_message'], model.search_val_list)
        result_list.append({
            'reply_name': row['reply_name'],
            'reply_date': row['reply_date'],
            'reply_message': _add_highlights(row['reply_message'], model.search_val_list),
        })

    result.result_list = result_list
    return result


def _add_highlights(val, target_vals):
    """
    ハイライト表示

    Args:
        val:
        target_vals:

    Returns:

    """
    result = val
    for target_val in target_vals:
        pattern = re.compile(re.escape(target_val), re.IGNORECASE)
        result = pattern.sub(lambda match: f"<mark>{match.group()}</mark>", result)

    # サニタイズして返却
    allowed_tags = ['mark']
    return bleach.clean(result.replace('<!channel>', '< !channel>'), tags=set(allowed_tags))

