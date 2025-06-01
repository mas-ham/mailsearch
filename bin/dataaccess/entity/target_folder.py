"""
Entity：target_folder

create 2025/05/31 hamada
"""
import dataclasses


@dataclasses.dataclass
class TargetFolder:
    folder_id = None
    folder_path = None
    folder_type = None
    is_target = None

    def __init__(self, folder_id = None, folder_path = None, folder_type = None, is_target = None):
        self.folder_id = folder_id
        self.folder_path = folder_path
        self.folder_type = folder_type
        self.is_target = is_target
