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

from common import const
from dataaccess.common.set_cond_model import Condition
from dataaccess.general.target_folder_dataaccess import TargetFolderDataAccess
from dataaccess.general.target_sender_dataaccess import TargetSenderDataAccess
from dataaccess.entity.target_folder import TargetFolder
from dataaccess.entity.target_sender import TargetSender
from dataaccess.ext.settings_dataaccess import SettingsDataaccess
from mailsearch.models import MailSearchModel, SlackDetailModel, SlackResultModel


def get_folder_list(conn):

    pythoncom.CoInitialize() # type: ignore
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    folder_list = []

    def search_folder(folder, folder_path=""):
        current_path = f"{folder_path}\\{folder.Name}" if folder_path else folder.Name
        # print(current_path)

        # データがなければInsert
        _insert_if_not_exists_folder(conn, current_path)

        # 現在データを取得
        target_folder = _get_folder_by_path(conn, current_path)
        # print(target_folder.folder_id)

        folder_list.append({
            'folder_id': target_folder.folder_id,
            'folder_path': current_path,
            'is_target': target_folder.is_target,
            'checked': 'checked' if target_folder.is_target else ''
        })

        for subfolder in folder.Folders:
            search_folder(subfolder, current_path)


    # 開始：受信トレイから再帰的に検索
    search_folder(inbox)

    return folder_list


def get_sender_list(conn):
    settings_dataaccess = SettingsDataaccess(conn)
    all_sender_list = settings_dataaccess.get_distinct_sender_list()

    sender_list = []
    for _, row in all_sender_list.iterrows():
        # email_address = row['email_address']
        # # データがなければInsert
        # _insert_if_not_exists_sender(conn, email_address)
        #
        # # 現在データを取得
        # target_sender = _get_sender_by_email_address(conn, email_address)
        # print(target_folder.folder_id)

        sender_list.append({
            'sender_id': row['sender_id'],
            'email_address': row['email_address'],
            'display_name': row['display_name'],
            'checked_display': 'checked' if row['is_display'] else '',
            'checked_check': 'checked' if row['is_checked'] else '',
        })

    return sender_list




def _insert_if_not_exists_folder(conn, folder_path):
    now_data = _get_folder_by_path(conn, folder_path)
    if now_data is not None:
        return

    entity = TargetFolder()
    entity.folder_path = folder_path
    entity.is_target = 0

    dataaccess = TargetFolderDataAccess(conn)
    dataaccess.insert(entity)


def _get_folder_by_path(conn, folder_path):
    dataaccess = TargetFolderDataAccess(conn)
    cond = [Condition('folder_path', folder_path)]
    results = dataaccess.select(conditions=cond)

    return results[0] if results else None


def _insert_if_not_exists_sender(conn, email_address):
    now_data = _get_sender_by_email_address(conn, email_address)
    if now_data is not None:
        return

    entity = TargetSender()
    entity.email_address = email_address
    entity.display_name = email_address
    entity.is_display = 0
    entity.is_checked = 0

    dataaccess = TargetSenderDataAccess(conn)
    dataaccess.insert(entity)


def _get_sender_by_email_address(conn, email_address):
    dataaccess = TargetSenderDataAccess(conn)
    cond = [Condition('email_address', email_address)]
    results = dataaccess.select(conditions=cond)

    return results[0] if results else None


def regist(conn, is_target_selected):
    """
    検索設定保存

    Args:
        conn:
        is_target_selected:

    Returns:

    """
    # フォルダー
    target_folder_dataaccess = TargetFolderDataAccess(conn)
    target_folder_list = target_folder_dataaccess.select_all()
    for target_folder in target_folder_list:
        folder_id = target_folder.folder_id
        # 更新用エンティティ
        entity = TargetFolder()
        entity.is_target = 1 if str(folder_id) in is_target_selected else 0
        # Update
        target_folder_dataaccess.update_selective(entity, folder_id)
