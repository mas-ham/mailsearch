"""
メール検索設定用dataaccess

"""
import pandas as pd

# 差出人一覧を取得
SQL_GET_SENDER_LIST = (
    """
    SELECT
        sender_info.sender                            AS email_address
      , sender_info.sender_name                       AS display_name
      , CASE WHEN target.sender_id IS NULL THEN 0
                                           ELSE target.is_display 
                                           END        AS is_display
      , CASE WHEN target.sender_id IS NULL THEN 0
                                           ELSE target.is_checked 
                                           END        AS is_checked
    FROM
      (
        SELECT
            mail.sender                   AS sender
          , MIN(mail.sender_name)         AS sender_name
        FROM
          tr_mail_messages                mail
        WHERE
              mail.sender NOT LIKE '/%'
          AND mail.sender <> ''
        GROUP BY
            mail.sender
      ) sender_info
      LEFT OUTER JOIN target_sender  target
        ON  target.email_address     = sender_info.sender
    ORDER BY
        sender_info.sender
    """
)

# 表示名取得
SQL_GET_SENDER_NAME = (
    """
    SELECT
        MIN(mail.sender_name)         AS sender_name
    FROM
      tr_mail_messages                mail
    WHERE
          mail.sender = ?
    GROUP BY
        mail.sender
    """
)



class SettingsDataaccess:
    def __init__(self, conn):
        self.conn = conn

    def get_sender_list(self):
        """
        差出人一覧を取得

        Returns:

        """
        return pd.read_sql(SQL_GET_SENDER_LIST, self.conn)

    def get_sender_name(self, email_address) -> str:
        """
        差出人名を取得

        Args:
            email_address:

        Returns:

        """
        results = pd.read_sql(SQL_GET_SENDER_NAME, self.conn, params=[email_address])
        if results.empty:
            return ''

        return results.iloc[0, 0]

