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
from dataaccess.entity.target_folder import TargetFolder
from mailsearch.models import MailSearchModel, SlackDetailModel, SlackResultModel


def get_folder_list(conn):

    pythoncom.CoInitialize()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    folder_list = []

    def search_folder(folder, folder_path=""):
        current_path = f"{folder_path}\\{folder.Name}" if folder_path else folder.Name
        print(current_path)

        # データがなければInsert
        _insert_if_not_exists(conn, current_path)

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


def _insert_if_not_exists(conn, folder_path):
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
        entity.is_target = 1 if folder_id in is_target_selected else 0
        # Update
        target_folder_dataaccess.update_selective(entity, folder_id)
