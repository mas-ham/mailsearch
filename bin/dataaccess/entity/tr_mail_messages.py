"""
Entity：tr_mail_messages

create 2025/05/25 hamada
"""
import dataclasses


@dataclasses.dataclass
class TrMailMessages:
    sender = None
    received = None
    subject = None
    body = None
    folder_path = None

    def __init__(self, sender = None, received = None, subject = None, body = None, folder_path = None):
        self.sender = sender
        self.received = received
        self.subject = subject
        self.body = body
        self.folder_path = folder_path
