"""
メールを取得する

create 2025/05/24 hamada
"""
import datetime

import pythoncom
import win32com.client
import dateutil

from common import const, shared_service, sql_shared_service
from common.logger.logger import Logger
from app_common import app_shared_service
from dataaccess.common.set_cond_model import Condition
from dataaccess.general.target_folder_dataaccess import TargetFolderDataAccess
from dataaccess.general.tr_mail_messages_dataaccess import TrMailMessagesDataAccess
from dataaccess.ext.export_dataaccess import ExportDataaccess
from dataaccess.entity.tr_mail_messages import TrMailMessages


class GetMessages:
    def __init__(self, logger:Logger, root_dir, bin_dir):
        self.logger = logger
        self.root_dir = root_dir
        self.bin_dir = bin_dir

        # 設定ファイル
        self.conf = app_shared_service.get_conf(self.root_dir)['get_messages']


    def main(self):
        """
        メールを取得

        Returns:

        """
        pythoncom.CoInitialize() # type: ignore
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

        # 期間を取得
        oldest, latest = self.get_term()

        # 受信ボックス/送信ボックスからメールを取得
        with sql_shared_service.get_connection(self.root_dir) as conn:
            target_folders = _get_target_folders(conn)

            # トランザクションを開始
            conn.execute('BEGIN TRANSACTION')

            for target_folder in target_folders:
                folder_type = target_folder.folder_type
                # フォルダを特定
                folder = outlook.GetDefaultFolder(folder_type)
                for subfolder_name in target_folder.folder_path.split("\\")[1:]:
                    folder = folder.Folders[subfolder_name]

                # 受信トレイから再帰的に検索
                self._search_folder(conn, folder, target_folder.folder_id, folder_type, oldest, latest)

            conn.commit()

        # 設定ファイル更新
        # from_dateを当日に更新する
        if int(self.conf['is_overwrite_from_date']):
            json_data = app_shared_service.get_conf(self.root_dir)
            json_data['get_messages']['from_date'] = datetime.datetime.now().strftime('%Y/%m/%d')
            app_shared_service.write_conf(self.root_dir, const.SETTINGS_FILENAME, json_data)


    def _search_folder(self, conn, folder, folder_id, folder_type, oldest, latest):
        """
        Outlookメールを取得し登録する

        Args:
            conn:
            folder:
            folder_id:
            folder_type:
            oldest:
            latest:

        Returns:

        """
        print(folder)

        messages = folder.Items
        # フィルタ
        if app_shared_service.is_inbox(folder_type):
            restriction = "[ReceivedTime] >= '" + oldest + "' AND [ReceivedTime] <= '" + latest + "'"
        else:
            restriction = "[SentOn] >= '" + oldest + "' AND [SentOn] <= '" + latest + "'"
        filtered_items = messages.Restrict(restriction)

        try:
            store_id = _get_store_id_from_folder(folder)
            for mail in filtered_items:
                if mail.Class != 43:
                    continue

                if app_shared_service.is_inbox(folder_type):
                    received = mail.ReceivedTime.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    received = mail.SentOn.strftime('%Y-%m-%d %H:%M:%S')

                from_email_address, from_display_name = _get_from_email(mail)
                to_list, cc_list = _get_recipients_addresses(mail)
                # Create Entity
                entity = TrMailMessages()
                entity.entry_id = mail.EntryID
                entity.store_id = store_id
                entity.received = received
                entity.sender = from_email_address
                entity.sender_name = from_display_name.strip()
                entity.to_email = ';'.join(to_list)
                entity.cc_email = ';'.join(cc_list)
                entity.subject = mail.Subject
                entity.body = mail.Body
                entity.folder_id = folder_id
                # Upsert
                dataaccess = ExportDataaccess(conn)
                dataaccess.upsert_mail_messages(entity)


        except Exception as e:
            # アイテムアクセス不可でも無視
            shared_service.print_except(e, self.logger)


    def get_term(self):
        """
        投稿内容取得期間を取得

        Returns:

        """
        from_date = self.conf['from_date']
        to_date = self.conf['to_date']
        if not from_date:
            # Fromが空の場合は1週間前を指定する
            from_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y/%m/%d')
        if not to_date:
            # Toが空の場合は当日を指定する
            to_date = datetime.datetime.now().strftime('%Y/%m/%d')

        self.logger.info(f'get_messages : {from_date} - {to_date}', is_print=True)

        # Outlook用の書式に変換
        oldest = dateutil.parser.parse(from_date).strftime('%m/%d/%Y %H:%M')
        latest = dateutil.parser.parse(to_date).strftime('%m/%d/%Y %H:%M')

        return oldest, latest


def _get_from_email(mail):
    """
    Fromのメールアドレスを取得

    Args:
        mail:

    Returns:

    """
    try:
        if mail.SenderEmailType == 'EX':  # Exchangeの場合
            exchange_user = mail.Sender.GetExchangeUser()
            email_address = exchange_user.PrimarySmtpAddress
            display_name = mail.sendername
        else:
            email_address = mail.SenderEmailAddress
            display_name = mail.sendername
        return email_address, display_name
    except Exception as e:
        shared_service.print_except(e)
        email_address = mail.SenderEmailAddress
        display_name = mail.sendername
        return email_address, display_name


def _get_recipients_email(recipient):
    """
    To、CCのメールアドレスを取得

    Args:
        recipient:

    Returns:

    """
    try:
        address_entry = recipient.AddressEntry
        if address_entry.Type == "EX":  # Exchangeのアドレス
            # Exchangeユーザー
            exchange_user = address_entry.GetExchangeUser()
            if exchange_user:
                return exchange_user.PrimarySmtpAddress if exchange_user.PrimarySmtpAddress == address_entry.Name else f'{address_entry.Name}<{exchange_user.PrimarySmtpAddress}>'
            else:
                # 配布リスト
                exchange_dist_list = address_entry.GetExchangeDistributionList()
                if exchange_dist_list is not None:
                    # SMTPアドレスが未割当の場合は表示名を返却
                    return exchange_dist_list.PrimarySmtpAddress if exchange_dist_list.PrimarySmtpAddress else address_entry.Name
        else:
            # 通常のSMTPアドレス
            return recipient.Address
    except Exception as e:
        shared_service.print_except(e)
        return ''

    return recipient.Address


def _get_recipients_addresses(mail):
    """
    メールのToおよびCCのSMTPアドレス一覧を取得

    Args:
        mail:

    Returns:

    """
    to_list = []
    cc_list = []

    for recipient in mail.Recipients:
        address = _get_recipients_email(recipient)
        if address is None:
            continue
        if recipient.Type == 1:
            # To
            to_list.append(address)
        elif recipient.Type == 2:
            # CC
            cc_list.append(address)

    return to_list, cc_list


def _get_store_id_from_folder(folder):
    """
    フォルダのStoreIDを取得

    Args:
        folder:

    Returns:

    """
    try:
        return folder.StoreID
    except Exception as e:
        print(f"Error getting StoreID: {e}")
        return None


def _get_target_folders(conn):
    """
    取得対象フォルダを取得

    Args:
        conn:

    Returns:

    """
    dataaccess = TargetFolderDataAccess(conn)
    cond = [
        Condition('is_target', 1),
    ]
    return dataaccess.select(conditions=cond)


def _get_mail_messages_by_pk(conn, entry_id, store_id):
    """
    メッセージを主キーで取得

    Args:
        conn:
        entry_id:
        store_id:

    Returns:

    """
    dataaccess = TrMailMessagesDataAccess(conn)
    return dataaccess.select_by_pk(entry_id, store_id)

