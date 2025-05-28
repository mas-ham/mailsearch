"""
Entity：target_folder

create 2025/05/28 hamada
"""
import dataclasses


@dataclasses.dataclass
class TargetFolder:
    folder_id = None
    folder_path = None
    is_target = None

    def __init__(self, folder_id = None, folder_path = None, is_target = None):
        self.folder_id = folder_id
        self.folder_path = folder_path
        self.is_target = is_target
