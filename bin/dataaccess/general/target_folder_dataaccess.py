"""
dataaccess：target_folder

create 2025/06/02 hamada
"""
from dataaccess.common.base_dataaccess import BaseDataAccess
from dataaccess.entity.target_folder import TargetFolder


TABLE_ID = 'target_folder'

class TargetFolderDataAccess(BaseDataAccess):
    def __init__(self, conn):
        super().__init__(conn)

        self.col_list = [
            'folder_path',
            'folder_type',
            'is_target',
        ]


    def select(self, conditions: list, order_by_list = None) -> list[TargetFolder]:
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
        return [TargetFolder(row['folder_id'], row['folder_path'], row['folder_type'], row['is_target']) for row in results]


    def select_by_pk(self, folder_id) -> TargetFolder | None:
        """
        Select_by_PK

        Args:
            folder_id:

        Returns:

        """
        result = self.execute_select_by_pk(TABLE_ID, folder_id = folder_id)
        if result is None:
            return None
        return TargetFolder(result['folder_id'], result['folder_path'], result['folder_type'], result['is_target'])


    def select_all(self, order_by_list = None) -> list[TargetFolder]:
        """
        Select_all

        Args:
            order_by_list:

        Returns:

        """
        results = self.execute_select_all(TABLE_ID, order_by_list)
        if not results:
            return []
        return [TargetFolder(row['folder_id'], row['folder_path'], row['folder_type'], row['is_target']) for row in results]


    def insert(self, entity: TargetFolder) -> int:
        """
        Insert

        Args:
            entity:

        Returns:

        """
        params = (
            entity.folder_path,
            entity.folder_type,
            entity.is_target,
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
                    entity.folder_path,
                    entity.folder_type,
                    entity.is_target,
                )
            )
        self.execute_insert_many(TABLE_ID, self.col_list, params)


    def update(self, entity: TargetFolder, folder_id):
        """
        Update

        Args:
            entity:
            folder_id:

        Returns:

        """
        update_info = {
            'folder_path': entity.folder_path,
            'folder_type': entity.folder_type,
            'is_target': entity.is_target,
        }
        self.execute_update(TABLE_ID, update_info, folder_id = folder_id)


    def update_selective(self, entity: TargetFolder, folder_id):
        """
        Update selective

        Args:
            entity:
            folder_id:

        Returns:

        """
        update_info = {}
        if entity.folder_path is not None:
            update_info['folder_path'] = entity.folder_path
        if entity.folder_type is not None:
            update_info['folder_type'] = entity.folder_type
        if entity.is_target is not None:
            update_info['is_target'] = entity.is_target

        self.execute_update(TABLE_ID, update_info, folder_id = folder_id)


    def delete(self, key: TargetFolder):
        """
        Delete

        Args:
            key:

        Returns:

        """
        key_map = {}
        if key.folder_id is not None:
            key_map['folder_id'] = key.folder_id
        if key.folder_path is not None:
            key_map['folder_path'] = key.folder_path
        if key.folder_type is not None:
            key_map['folder_type'] = key.folder_type
        if key.is_target is not None:
            key_map['is_target'] = key.is_target

        self.execute_delete(TABLE_ID, **key_map)


    def delete_by_pk(self, folder_id):
        """
        Delete_by_PK

        Args:
            folder_id:

        Returns:

        """
        self.execute_delete(TABLE_ID, folder_id = folder_id)


    def delete_all(self):
        """
        Delete_All

        Args:

        Returns:

        """
        self.execute_delete_all(TABLE_ID)

