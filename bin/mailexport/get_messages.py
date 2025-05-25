"""
メールを取得する

create 2025/05/24 hamada
"""
import datetime

import pythoncom
import win32com.client
import dateutil

from common import shared_service, sql_shared_service
from common.logger.logger import Logger
from app_common import app_shared_service
from dataaccess.common.set_cond_model import Condition
from dataaccess.general.target_folder_dataaccess import TargetFolderDataAccess
from dataaccess.general.tr_mail_messages_dataaccess import TrMailMessagesDataAccess
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
        inbox = outlook.GetDefaultFolder(6)

        # 期間を取得
        oldest, latest = self.get_term()

        def search_folder(folder, folder_path=""):
            current_path = f"{folder_path}\\{folder.Name}" if folder_path else folder.Name
            print(current_path)

            if current_path in target_folders:

                messages = folder.Items
                # フィルタ
                restriction = "[ReceivedTime] >= '" + oldest + "' AND [ReceivedTime] <= '" + latest + "'"
                filtered_items = messages.Restrict(restriction)

                try:
                    for mail in filtered_items:
                        # print(mail.ReceivedTime)
                        received = mail.ReceivedTime.strftime('%Y-%m-%d %H:%M:%S')
                        # print(received)
                        org = _get_mail_messages_by_pk(conn, mail.SenderEmailAddress, received, mail.Subject)

                        if org is None:
                            # Insert
                            entity = TrMailMessages()
                            entity.sender = mail.SenderEmailAddress # Sender.Name
                            entity.received = received
                            entity.subject = mail.Subject
                            entity.body = mail.Body
                            entity.folder_path = current_path

                            _insert_mail_messages(conn, entity)

                except Exception as e:
                    # アイテムアクセス不可でも無視
                    shared_service.print_except(e, self.logger)

            for subfolder in folder.Folders:
                search_folder(subfolder, current_path)

        with sql_shared_service.get_connection(self.root_dir) as conn:
            target_folders = _get_target_folders(conn)

            # 受信トレイから再帰的に検索
            search_folder(inbox)

            conn.commit()


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


def _get_target_folders(conn):
    dataaccess = TargetFolderDataAccess(conn)
    cond = [Condition('is_target', 1)]
    return [r.folder_path for r in dataaccess.select(conditions=cond)]

def _get_mail_messages_by_pk(conn, sender, received, subject):
    dataaccess = TrMailMessagesDataAccess(conn)
    return dataaccess.select_by_pk(sender, received, subject)


def _insert_mail_messages(conn, entity: TrMailMessages):
    dataaccess = TrMailMessagesDataAccess(conn)
    dataaccess.insert(entity)