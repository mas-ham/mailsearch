"""
メール検索用dataaccess

"""
import pandas as pd

from mailsearch.models import MailSearchModel

# 検索
SQL_SEARCH = (
    """
    SELECT
        mail.entry_id
      , mail.store_id
      , mail.received
      , mail.sender
      , mail.sender_name
      , mail.to_email
      , mail.cc_email
      , mail.subject
      , mail.body
      , mail.folder_id
      , folder.folder_path
    FROM
      tr_mail_messages               mail
      LEFT OUTER JOIN target_folder  folder
        ON  folder.folder_id           = mail.folder_id
    WHERE
          1 = 1
    {}
    ORDER BY
        mail.received
      , folder.folder_path
    """
)




class SearchDataaccess:
    def __init__(self, conn):
        self.conn = conn

    def search(self, model: MailSearchModel) -> pd.DataFrame:
        """
        検索

        Args:

        Returns:

        """
        # SQLを組み立て
        sql_where = ''
        params = []
        if model.folder_list:
            # フォルダー
            placeholder_list = ['?' for _ in model.folder_list]
            val_list = [v for v in model.folder_list]
            sql_where += f'      AND mail.folder_id IN ({", ".join(placeholder_list)}) '
            params.extend(val_list)
        if model.sender_list:
            # 差出人
            placeholder_list = ['?' for _ in model.sender_list]
            val_list = [v for v in model.sender_list]
            sql_where += f'\n      AND mail.sender IN ({", ".join(placeholder_list)}) '
            params.extend(val_list)
        if model.search_val_list:
            # 検索文字列
            search_list = []
            cond = f' AND ' if model.search_type == '01' else ' OR '
            if model.is_target_title:
                list_ = []
                for search_val in model.search_val_list:
                    list_.append(f"mail.subject LIKE ?")
                    params.append(f'%{search_val}%')
                cond_str = cond.join(list_)
                search_list.append(f'({cond_str})')
                # sql_where += f'\n      AND ({cond_str}) '
            if model.is_target_body:
                list_ = []
                for search_val in model.search_val_list:
                    list_.append(f"mail.body LIKE ?")
                    params.append(f'%{search_val}%')
                cond_str = cond.join(list_)
                search_list.append(f'({cond_str})')
                # sql_where += f'\n      OR  ({cond_str}) '

            sql_where += f'\n      AND ({" OR ".join(search_list)}) '
        sql = SQL_SEARCH.format(sql_where)
        print(sql)

        # 実行
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return pd.DataFrame(cursor.fetchall(), columns=['entry_id', 'store_id', 'received', 'sender', 'sender_name', 'to_email', 'cc_email', 'subject', 'body', 'folder_id', 'folder_path'])

