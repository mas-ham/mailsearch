"""
メールから検索する

create 2025/05/24 hamada
"""
import re

import bleach

from mailsearch.models import MailSearchModel, MailDetailModel, MailResultModel
from dataaccess.ext.search_dataaccess import SearchDataaccess
from dataaccess.general.target_sender_dataaccess import TargetSenderDataAccess
from dataaccess.general.target_folder_dataaccess import TargetFolderDataAccess
from dataaccess.common.set_cond_model import Condition
from dataaccess.common.set_sort_model import OrderBy


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


def search(conn, model: MailSearchModel):
    """
    検索

    Args:
        conn:
        model:

    Returns:

    """

    # 検索
    dataaccess = SearchDataaccess(conn)
    results = dataaccess.search(model)

    return _convert_to_json_for_search(results, model.search_val_list)


def _convert_to_json_for_search(record_list, search_val_list):
    """
    検索結果画面に返却する用にJSONへコンバート
    Args:
        record_list:

    Returns:

    """
    if not record_list:
        return []

    result_list = []
    for row in record_list:
        result_list.append({
            'folder_path': row['folder_path'],
            'sender': row['sender'] if row['sender'] == row['sender_name'] else f"{row['sender_name']}<{row['sender']}>",
            'sender_name': row['sender_name'],
            'received': row['received'],
            'subject': _add_highlights(row['subject'], search_val_list),
            'entry_id': row['entry_id'],
            'store_id': row['store_id'],
        })

    return result_list


def get_detail(conn, model: MailDetailModel) -> MailResultModel:
    """
    詳細を取得

    Args:
        conn:
        model:

    Returns:

    """
    # 検索
    dataaccess = SearchDataaccess(conn)
    record = dataaccess.detail(model.entry_id, model.store_id)

    result = MailResultModel()
    result.received = record['received']
    result.folder_path = record['folder_path']
    result.sender = record['sender']
    result.sender_name = record['sender_name']
    result.to_email = record['to_email']
    result.cc_email = record['cc_email']
    result.subject = _add_highlights(record['subject'], model.search_val_list)
    result.body = _add_highlights(record['body'], model.search_val_list)

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

