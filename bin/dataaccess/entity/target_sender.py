"""
Entity：target_sender

create 2025/06/04 13:31:05 generator
"""
import dataclasses

@dataclasses.dataclass
class TargetSender:
    sender_id: int = None
    email_address: str = None
    display_name: str = None
    is_display: int = None
    is_checked: int = None
