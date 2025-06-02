"""
dataaccess：tr_mail_messages

create 2025/06/02 hamada
"""
from dataaccess.common.base_dataaccess import BaseDataAccess
from dataaccess.entity.tr_mail_messages import TrMailMessages


TABLE_ID = 'tr_mail_messages'

class TrMailMessagesDataAccess(BaseDataAccess):
    def __init__(self, conn):
        super().__init__(conn)

        self.col_list = [
            'entry_id',
            'store_id',
            'received',
            'sender',
            'sender_name',
            'to_email',
            'cc_email',
            'subject',
            'body',
            'folder_id',
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
        if not results:
            return []
        return [TrMailMessages(row['entry_id'], row['store_id'], row['received'], row['sender'], row['sender_name'], row['to_email'], row['cc_email'], row['subject'], row['body'], row['folder_id']) for row in results]


    def select_by_pk(self, entry_id, store_id) -> TrMailMessages | None:
        """
        Select_by_PK

        Args:
            entry_id:
            store_id:

        Returns:

        """
        result = self.execute_select_by_pk(TABLE_ID, entry_id = entry_id, store_id = store_id)
        if result is None:
            return None
        return TrMailMessages(result['entry_id'], result['store_id'], result['received'], result['sender'], result['sender_name'], result['to_email'], result['cc_email'], result['subject'], result['body'], result['folder_id'])


    def select_all(self, order_by_list = None) -> list[TrMailMessages]:
        """
        Select_all

        Args:
            order_by_list:

        Returns:

        """
        results = self.execute_select_all(TABLE_ID, order_by_list)
        if not results:
            return []
        return [TrMailMessages(row['entry_id'], row['store_id'], row['received'], row['sender'], row['sender_name'], row['to_email'], row['cc_email'], row['subject'], row['body'], row['folder_id']) for row in results]


    def insert(self, entity: TrMailMessages) -> int:
        """
        Insert

        Args:
            entity:

        Returns:

        """
        params = (
            entity.entry_id,
            entity.store_id,
            entity.received,
            entity.sender,
            entity.sender_name,
            entity.to_email,
            entity.cc_email,
            entity.subject,
            entity.body,
            entity.folder_id,
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
                    entity.entry_id,
                    entity.store_id,
                    entity.received,
                    entity.sender,
                    entity.sender_name,
                    entity.to_email,
                    entity.cc_email,
                    entity.subject,
                    entity.body,
                    entity.folder_id,
                )
            )
        self.execute_insert_many(TABLE_ID, self.col_list, params)


    def update(self, entity: TrMailMessages, entry_id, store_id):
        """
        Update

        Args:
            entity:
            entry_id:
            store_id:

        Returns:

        """
        update_info = {
            'entry_id': entity.entry_id,
            'store_id': entity.store_id,
            'received': entity.received,
            'sender': entity.sender,
            'sender_name': entity.sender_name,
            'to_email': entity.to_email,
            'cc_email': entity.cc_email,
            'subject': entity.subject,
            'body': entity.body,
            'folder_id': entity.folder_id,
        }
        self.execute_update(TABLE_ID, update_info, entry_id = entry_id, store_id = store_id)


    def update_selective(self, entity: TrMailMessages, entry_id, store_id):
        """
        Update selective

        Args:
            entity:
            entry_id:
            store_id:

        Returns:

        """
        update_info = {}
        if entity.entry_id is not None:
            update_info['entry_id'] = entity.entry_id
        if entity.store_id is not None:
            update_info['store_id'] = entity.store_id
        if entity.received is not None:
            update_info['received'] = entity.received
        if entity.sender is not None:
            update_info['sender'] = entity.sender
        if entity.sender_name is not None:
            update_info['sender_name'] = entity.sender_name
        if entity.to_email is not None:
            update_info['to_email'] = entity.to_email
        if entity.cc_email is not None:
            update_info['cc_email'] = entity.cc_email
        if entity.subject is not None:
            update_info['subject'] = entity.subject
        if entity.body is not None:
            update_info['body'] = entity.body
        if entity.folder_id is not None:
            update_info['folder_id'] = entity.folder_id

        self.execute_update(TABLE_ID, update_info, entry_id = entry_id, store_id = store_id)


    def delete(self, key: TrMailMessages):
        """
        Delete

        Args:
            key:

        Returns:

        """
        key_map = {}
        if key.entry_id is not None:
            key_map['entry_id'] = key.entry_id
        if key.store_id is not None:
            key_map['store_id'] = key.store_id
        if key.received is not None:
            key_map['received'] = key.received
        if key.sender is not None:
            key_map['sender'] = key.sender
        if key.sender_name is not None:
            key_map['sender_name'] = key.sender_name
        if key.to_email is not None:
            key_map['to_email'] = key.to_email
        if key.cc_email is not None:
            key_map['cc_email'] = key.cc_email
        if key.subject is not None:
            key_map['subject'] = key.subject
        if key.body is not None:
            key_map['body'] = key.body
        if key.folder_id is not None:
            key_map['folder_id'] = key.folder_id

        self.execute_delete(TABLE_ID, **key_map)


    def delete_by_pk(self, entry_id, store_id):
        """
        Delete_by_PK

        Args:
            entry_id:
            store_id:

        Returns:

        """
        self.execute_delete(TABLE_ID, entry_id = entry_id, store_id = store_id)


    def delete_all(self):
        """
        Delete_All

        Args:

        Returns:

        """
        self.execute_delete_all(TABLE_ID)

