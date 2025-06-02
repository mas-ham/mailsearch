"""
SQL共通サービス

create 2023/11/01 TIS hamada
"""
import os
import re
import sqlite3

from common import shared_service

def get_connection(root_dir):
    """
    DB接続

    Returns:
        コネクション

    """

    # SQLite3
    return sqlite3.connect(os.path.join(root_dir, 'db', 'mailsearch.db'))


def get_query(query_file_path):
    """
    SQLファイルからクエリーを取得

    Args:
        query_file_path:

    Returns:
        SQLクエリー

    """
    with open(query_file_path, 'r', encoding='utf-8') as f:
        query = f.read()
    return query


def is_empty(val):
    """
    Null(空文字含む)かどうか

    Args:
        val:

    Returns:
        bool値(true: Null or 空文字)

    """

    return val is None or val == ''


def null_to_empty(val):
    """
    Nullを空文字に変換

    Args:
        val:

    Returns:
        変換後の値

    """

    if val is None:
        return ''
    return val


def write_sql_log(sql, *args):
    """
    SQLログ出力

    Args:
        sql:
        *args:

    Returns:

    """
    def clean_string(s):
        # 改行を半角スペースに置換
        s = s.replace('\n', ' ').replace('\r', ' ')
        # 複数の半角スペースを1つにまとめる
        s = re.sub(r' +', ' ', s)
        # 先頭・末尾の空白を除去
        return s.strip()

    try:
        logger = shared_service.set_sql_logger()
        logger.write_sql_log('', clean_string(sql), *args)
    except Exception as e:
        print(e)
        pass

