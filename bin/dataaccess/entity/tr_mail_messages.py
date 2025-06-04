"""
Entity：tr_mail_messages

create 2025/06/04 13:31:05 generator
"""
import dataclasses

@dataclasses.dataclass
class TrMailMessages:
    entry_id: str = None
    store_id: str = None
    received: str = None
    sender: str = None
    sender_name: str = None
    to_email: str = None
    cc_email: str = None
    subject: str = None
    body: str = None
    folder_id: int = None
