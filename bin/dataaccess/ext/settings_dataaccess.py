"""
メール検索設定用dataaccess

"""
import pandas as pd

# 差出人一覧を取得
SQL_GET_DISTINCT_SENDER_LIST = (
    """
    SELECT DISTINCT sender FROM tr_mail_messages WHERE sender NOT LIKE '/%' AND sender <> '' ORDER BY sender
    """
)


class SettingsDataaccess:
    def __init__(self, conn):
        self.conn = conn

    def get_distinct_sender_list(self):
        return pd.read_sql(SQL_GET_DISTINCT_SENDER_LIST, self.conn)

