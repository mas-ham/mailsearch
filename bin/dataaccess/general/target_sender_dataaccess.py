"""
dataaccess：target_sender

create 2025/06/02 hamada
"""
from dataaccess.common.base_dataaccess import BaseDataAccess
from dataaccess.entity.target_sender import TargetSender


TABLE_ID = 'target_sender'

class TargetSenderDataAccess(BaseDataAccess):
    def __init__(self, conn):
        super().__init__(conn)

        self.col_list = [
            'sender_id',
            'email_address',
            'display_name',
            'is_display',
            'is_checked',
        ]


    def select(self, conditions: list, order_by_list = None) -> list[TargetSender]:
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
        return [TargetSender(row['sender_id'], row['email_address'], row['display_name'], row['is_display'], row['is_checked']) for row in results]


    def select_by_pk(self, sender_id) -> TargetSender | None:
        """
        Select_by_PK

        Args:
            sender_id:

        Returns:

        """
        result = self.execute_select_by_pk(TABLE_ID, sender_id = sender_id)
        if result is None:
            return None
        return TargetSender(result['sender_id'], result['email_address'], result['display_name'], result['is_display'], result['is_checked'])


    def select_all(self, order_by_list = None) -> list[TargetSender]:
        """
        Select_all

        Args:
            order_by_list:

        Returns:

        """
        results = self.execute_select_all(TABLE_ID, order_by_list)
        if results.empty:
            return []
        return [TargetSender(row['sender_id'], row['email_address'], row['display_name'], row['is_display'], row['is_checked']) for row in results]


    def insert(self, entity: TargetSender) -> int:
        """
        Insert

        Args:
            entity:

        Returns:

        """
        params = (
            entity.sender_id,
            entity.email_address,
            entity.display_name,
            entity.is_display,
            entity.is_checked,
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
                    entity.sender_id,
                    entity.email_address,
                    entity.display_name,
                    entity.is_display,
                    entity.is_checked,
                )
            )
        self.execute_insert_many(TABLE_ID, self.col_list, params)


    def update(self, entity: TargetSender, sender_id):
        """
        Update

        Args:
            entity:
            sender_id:

        Returns:

        """
        update_info = {
            'sender_id': entity.sender_id,
            'email_address': entity.email_address,
            'display_name': entity.display_name,
            'is_display': entity.is_display,
            'is_checked': entity.is_checked,
        }
        self.execute_update(TABLE_ID, update_info, sender_id = sender_id)


    def update_selective(self, entity: TargetSender, sender_id):
        """
        Update selective

        Args:
            entity:
            sender_id:

        Returns:

        """
        update_info = {}
        if entity.sender_id is not None:
            update_info['sender_id'] = entity.sender_id
        if entity.email_address is not None:
            update_info['email_address'] = entity.email_address
        if entity.display_name is not None:
            update_info['display_name'] = entity.display_name
        if entity.is_display is not None:
            update_info['is_display'] = entity.is_display
        if entity.is_checked is not None:
            update_info['is_checked'] = entity.is_checked

        self.execute_update(TABLE_ID, update_info, sender_id = sender_id)


    def delete(self, key: TargetSender):
        """
        Delete

        Args:
            key:

        Returns:

        """
        key_map = {}
        if key.sender_id is not None:
            key_map['sender_id'] = key.sender_id
        if key.email_address is not None:
            key_map['email_address'] = key.email_address
        if key.display_name is not None:
            key_map['display_name'] = key.display_name
        if key.is_display is not None:
            key_map['is_display'] = key.is_display
        if key.is_checked is not None:
            key_map['is_checked'] = key.is_checked

        self.execute_delete(TABLE_ID, **key_map)


    def delete_by_pk(self, sender_id):
        """
        Delete_by_PK

        Args:
            sender_id:

        Returns:

        """
        self.execute_delete(TABLE_ID, sender_id = sender_id)


    def delete_all(self):
        """
        Delete_All

        Args:

        Returns:

        """
        self.execute_delete_all(TABLE_ID)

