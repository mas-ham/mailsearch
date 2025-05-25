"""
dataaccess：tr_mail_messages

create 2025/05/25 hamada
"""
from dataaccess.common.base_dataaccess import BaseDataAccess
from dataaccess.entity.tr_mail_messages import TrMailMessages


TABLE_ID = 'tr_mail_messages'

class TrMailMessagesDataAccess(BaseDataAccess):
    def __init__(self, conn):
        super().__init__(conn)

        self.col_list = [
            'sender',
            'received',
            'subject',
            'body',
            'folder_path',
        ]


    def select(self, conditions: list, order_by_list = None) -> list[TrMailMessages]:
        """
        Select

        Args:
            conditions:
            order_by_list:

        Returns:

        """

        results = self.execute_select(TABLE_ID, conditions, order_by_list)
        if results.empty:
            return []
        return [TrMailMessages(row['sender'], row['received'], row['subject'], row['body'], row['folder_path']) for _, row in results.iterrows()]


    def select_by_pk(self, sender, received, subject) -> TrMailMessages | None:
        """
        Select_by_PK

        Args:
            sender:
            received:
            subject:

        Returns:

        """
        results = self.execute_select_by_pk(TABLE_ID, sender = sender, received = received, subject = subject)
        if results.empty:
            return None
        return TrMailMessages(results.iat[0, 0], results.iat[0, 1], results.iat[0, 2], results.iat[0, 3], results.iat[0, 4])


    def select_all(self, order_by_list = None) -> list[TrMailMessages]:
        """
        Select_all

        Args:
            order_by_list:

        Returns:

        """
        results = self.execute_select_all(TABLE_ID, order_by_list)
        if results.empty:
            return []
        return [TrMailMessages(row['sender'], row['received'], row['subject'], row['body'], row['folder_path']) for _, row in results.iterrows()]


    def insert(self, entity: TrMailMessages) -> int:
        """
        Insert

        Args:
            entity:

        Returns:

        """
        params = (
            entity.sender,
            entity.received,
            entity.subject,
            entity.body,
            entity.folder_path,
        )
        return self.execute_insert(TABLE_ID, self.col_list, params)


    def insert_many(self, entity_list: list):
        """
        Insert_many

        Args:
            entity_list:

        Returns:

        """
        params = []
        for entity in entity_list:
            params.append(
                (
                    entity.sender,
                    entity.received,
                    entity.subject,
                    entity.body,
                    entity.folder_path,
                )
            )
        self.execute_insert_many(TABLE_ID, self.col_list, params)


    def update(self, entity: TrMailMessages, sender, received, subject):
        """
        Update

        Args:
            entity:
            sender:
            received:
            subject:

        Returns:

        """
        update_info = {
            'sender': entity.sender,
            'received': entity.received,
            'subject': entity.subject,
            'body': entity.body,
            'folder_path': entity.folder_path,
        }
        self.execute_update(TABLE_ID, update_info, sender = sender, received = received, subject = subject)


    def update_selective(self, entity: TrMailMessages, sender, received, subject):
        """
        Update selective

        Args:
            entity:
            sender:
            received:
            subject:

        Returns:

        """
        update_info = {}
        if entity.sender is not None:
            update_info['sender'] = entity.sender
        if entity.received is not None:
            update_info['received'] = entity.received
        if entity.subject is not None:
            update_info['subject'] = entity.subject
        if entity.body is not None:
            update_info['body'] = entity.body
        if entity.folder_path is not None:
            update_info['folder_path'] = entity.folder_path

        self.execute_update(TABLE_ID, update_info, sender = sender, received = received, subject = subject)


    def delete(self, key: TrMailMessages):
        """
        Delete

        Args:
            key:

        Returns:

        """
        key_map = {}
        if key.sender is not None:
            key_map['sender'] = key.sender
        if key.received is not None:
            key_map['received'] = key.received
        if key.subject is not None:
            key_map['subject'] = key.subject
        if key.body is not None:
            key_map['body'] = key.body
        if key.folder_path is not None:
            key_map['folder_path'] = key.folder_path

        self.execute_delete(TABLE_ID, **key_map)


    def delete_by_pk(self, sender, received, subject):
        """
        Delete_by_PK

        Args:
            sender:
            received:
            subject:

        Returns:

        """
        self.execute_delete(TABLE_ID, sender = sender, received = received, subject = subject)


    def delete_all(self):
        """
        Delete_All

        Args:

        Returns:

        """
        self.execute_delete_all(TABLE_ID)

