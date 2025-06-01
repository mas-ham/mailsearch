"""
メール検索：設定

create 2025/05/24 hamada
"""
import pythoncom
import win32com.client

from common import const
from app_common import app_shared_service
from dataaccess.common.set_cond_model import Condition
from dataaccess.general.target_folder_dataaccess import TargetFolderDataAccess
from dataaccess.general.target_sender_dataaccess import TargetSenderDataAccess
from dataaccess.entity.target_folder import TargetFolder
from dataaccess.entity.target_sender import TargetSender
from dataaccess.ext.settings_dataaccess import SettingsDataaccess


def get_folder_list(conn):
    """
    フォルダー一覧を取得

    Args:
        conn:

    Returns:

    """

    folder_list = []

    def search_folder(folder_type, folder, folder_path=""):
        current_path = f"{folder_path}\\{folder.Name}" if folder_path else folder.Name

        # データがなければInsert
        _insert_if_not_exists_folder(conn, current_path, folder_type)

        # 現在データを取得
        target_folder = _get_folder_by_path(conn, current_path)

        folder_list.append({
            'folder_id': target_folder.folder_id,
            'folder_path': current_path,
            'folder_type': folder_type,
            'is_target': target_folder.is_target,
            'checked': 'checked' if target_folder.is_target else ''
        })

        for subfolder in folder.Folders:
            search_folder(folder_type, subfolder, current_path)

    pythoncom.CoInitialize() # type: ignore
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    # 受信トレイから再帰的に検索
    search_folder(const.INBOX, outlook.GetDefaultFolder(const.INBOX))

    # 送信トレイから再帰的に検索
    search_folder(const.SENT_BOX, outlook.GetDefaultFolder(const.SENT_BOX))

    # フォルダーパスでソートして返却
    return sorted(folder_list, key=lambda x: (-x['folder_type'], x['folder_path']))


def get_sender_list(conn):
    """
    差出人一覧を取得

    Args:
        conn:

    Returns:

    """
    settings_dataaccess = SettingsDataaccess(conn)
    all_sender_list = settings_dataaccess.get_sender_list()

    sender_list = []
    for _, row in all_sender_list.iterrows():
        sender_list.append({
            # 'sender_id': row['sender_id'],
            'domain': app_shared_service.extract_domain(row['email_address']),
            'email_address': row['email_address'],
            'display_name': row['display_name'],
            'is_display': 'checked' if row['is_display'] else '',
            'is_checked': 'checked' if row['is_checked'] else '',
        })

    return sorted(sender_list, key=lambda x: (x['domain'], x['email_address']))


def _insert_if_not_exists_folder(conn, folder_path, folder_type):
    """
    対象フォルダー管理に存在しないデータを登録する

    Args:
        conn:
        folder_path:
        folder_type:

    Returns:

    """
    now_data = _get_folder_by_path(conn, folder_path)
    if now_data is not None:
        return

    entity = TargetFolder()
    entity.folder_path = folder_path
    entity.folder_type = folder_type
    entity.is_target = 0

    dataaccess = TargetFolderDataAccess(conn)
    dataaccess.insert(entity)


def _get_folder_by_path(conn, folder_path):
    """
    対象フォルダー管理からパスでデータを取得する

    Args:
        conn:
        folder_path:

    Returns:

    """
    dataaccess = TargetFolderDataAccess(conn)
    cond = [Condition('folder_path', folder_path)]
    results = dataaccess.select(conditions=cond)

    return results[0] if results else None


def regist(conn, is_target_selected, is_sender_display_selected, is_sender_checked_selected):
    """
    検索設定保存

    Args:
        conn:
        is_target_selected:
        is_sender_display_selected:
        is_sender_checked_selected:

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

    # 差出人
    target_sender_dataaccess = TargetSenderDataAccess(conn)
    target_sender_list = target_sender_dataaccess.select_all()
    sender_list = [record.email_address for record in target_sender_list]

    # チェックOFF
    for email_address in sender_list:
        # 表示、初期値の両方に存在しない場合、チェックをOFFに更新する
        if email_address not in is_sender_display_selected and email_address not in is_sender_checked_selected:
            entity = TargetSender()
            entity.is_display = 0
            entity.is_checked = 0
            target_sender_dataaccess.update_selective(entity, _get_sender_id_by_email_address(target_sender_list, email_address))

    # チェックON
    update_list = []
    for email_address in is_sender_display_selected:
        update_list.append({
            'email_address': email_address,
            'is_display': 1,
            'is_checked': 0,
        })

    for email_address in is_sender_checked_selected:
        for record in update_list:
            if email_address == record['email_address']:
                record['is_checked'] = 1
                break
        else:
            update_list.append({
            'email_address': email_address,
            'is_display': 0,
            'is_checked': 1,
            })

    for record in update_list:
        email_address = record['email_address']
        if email_address in sender_list:
            # Update
            entity = TargetSender()
            entity.is_display = record['is_display']
            entity.is_checked = record['is_checked']
            target_sender_dataaccess.update_selective(entity, _get_sender_id_by_email_address(target_sender_list, email_address))
        else:
            # Insert
            entity = TargetSender()
            entity.email_address = email_address
            entity.display_name = _get_display_name(conn, email_address)
            entity.is_display = record['is_display']
            entity.is_checked = record['is_checked']
            target_sender_dataaccess.insert(entity)


def _get_sender_id_by_email_address(sender_list: list[TargetSender], email_address):
    """
    EメールアドレスからIDを取得する

    Args:
        sender_list:
        email_address:

    Returns:

    """
    for record in sender_list:
        if email_address == record.email_address:
            return record.sender_id
    return None

def _get_display_name(conn, email_address):
    """
    Eメールアドレスから表示名を取得する

    Args:
        conn:
        email_address:

    Returns:

    """
    settings_dataaccess = SettingsDataaccess(conn)
    return settings_dataaccess.get_sender_name(email_address)

