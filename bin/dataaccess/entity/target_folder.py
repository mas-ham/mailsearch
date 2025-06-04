"""
Entity：target_folder

create 2025/06/04 13:31:05 generator
"""
import dataclasses

@dataclasses.dataclass
class TargetFolder:
    folder_id: int = None
    folder_path: str = None
    folder_type: int = None
    is_target: int = None
