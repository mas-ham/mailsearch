"""
インストール

create 2025/05/13 hamada
"""
import os


def install(bin_dir, conn):
    cur = conn.cursor()

    # テーブルcreate
    # __create_table(cur, bin_dir, 'target_folder')
    __create_table(cur, bin_dir, 'target_sender')
    __create_table(cur, bin_dir, 'tr_mail_messages')

    # インデックス
    cur.execute('CREATE INDEX idx_messages_sender ON tr_mail_messages(sender)')

    conn.commit()
    cur.close()


def __create_table(cur, bin_dir, table_id):
    """
    テーブルCreate
    """
    # drop
    cur.execute(__create_query_drop(table_id))
    # create
    cur.execute(__get_query(bin_dir, f'{table_id}.sql'))


def __create_query_drop(table_id):
    """
    Drop文取得
    """
    return f'DROP TABLE IF EXISTS {table_id}'


def __get_query(bin_dir, filename):
    """
    Create文取得
    """
    print(filename)
    with open(os.path.join(bin_dir, 'settings', 'ddl', filename), 'r', encoding='utf-8') as f:
        query = f.read()
    return query


