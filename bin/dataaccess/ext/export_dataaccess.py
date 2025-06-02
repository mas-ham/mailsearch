"""
メッセージ取得用dataaccess

"""
import sqlite3
from dataclasses import asdict

from dataaccess.entity.tr_mail_messages import TrMailMessages

# チャンネルを登録
SQL_UPSERT_MAIL_MESSAGES = (
    """
    INSERT INTO tr_mail_messages (
        entry_id
      , store_id
      , received
      , sender
      , sender_name
      , to_email
      , cc_email
      , subject
      , body
      , folder_id
    )
    VALUES (
        :entry_id
      , :store_id
      , :received
      , :sender
      , :sender_name
      , :to_email
      , :cc_email
      , :subject
      , :body
      , :folder_id
    )
    ON CONFLICT (entry_id, store_id)
    DO UPDATE 
        SET 
            received        = :received
          , sender          = :sender
          , sender_name     = :sender_name
          , to_email        = :to_email
          , cc_email        = :cc_email
          , subject         = :subject
          , body            = :body
          , folder_id       = :folder_id
    """
)

class ExportDataaccess:
    def __init__(self, conn):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row


    def upsert_mail_messages(self, entity: TrMailMessages):
        """
        メッセージ一覧Upsert

        Args:
            entity:

        Returns:

        """
        cursor = self.conn.cursor()
        cursor.execute(SQL_UPSERT_MAIL_MESSAGES, asdict(entity))
        cursor.close()
