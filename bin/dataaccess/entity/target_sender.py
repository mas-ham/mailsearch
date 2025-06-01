"""
Entity：target_sender

create 2025/06/02 hamada
"""
import dataclasses


@dataclasses.dataclass
class TargetSender:
    sender_id = None
    email_address = None
    display_name = None
    is_display = None
    is_checked = None

    def __init__(self, sender_id = None, email_address = None, display_name = None, is_display = None, is_checked = None):
        self.sender_id = sender_id
        self.email_address = email_address
        self.display_name = display_name
        self.is_display = is_display
        self.is_checked = is_checked
