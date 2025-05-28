"""
メール検索設定用dataaccess

"""
import pandas as pd

# 差出人一覧を取得
SQL_GET_DISTINCT_SENDER_LIST = (
    """
    SELECT
        DISTINCT
        mail.sender                                   AS email_address
      , mail.display_name                             AS display_name
      , CASE WHEN target.sender_id IS NULL THEN 0
                                           ELSE target.is_display 
                                           END        AS is_display
      , CASE WHEN target.sender_id IS NULL THEN 0
                                           ELSE target.is_checked 
                                           END        AS is_checked
    FROM
      tr_mail_messages               mail
      LEFT OUTER JOIN target_sender  target
        ON  target.email_address     = mail.sender
    WHERE
          mail.sender NOT LIKE '/%'
      AND mail.sender <> ''
    ORDER BY
        mail.sender
    """
)


class SettingsDataaccess:
    def __init__(self, conn):
        self.conn = conn

    def get_distinct_sender_list(self):
        return pd.read_sql(SQL_GET_DISTINCT_SENDER_LIST, self.conn)

