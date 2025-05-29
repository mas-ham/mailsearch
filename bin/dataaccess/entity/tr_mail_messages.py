"""
Entity：tr_mail_messages

create 2025/05/29 hamada
"""
import dataclasses


@dataclasses.dataclass
class TrMailMessages:
    entry_id = None
    store_id = None
    received = None
    sender = None
    sender_name = None
    to_email = None
    cc_email = None
    subject = None
    body = None
    folder_id = None

    def __init__(self, entry_id = None, store_id = None, received = None, sender = None, sender_name = None, to_email = None, cc_email = None, subject = None, body = None, folder_id = None):
        self.entry_id = entry_id
        self.store_id = store_id
        self.received = received
        self.sender = sender
        self.sender_name = sender_name
        self.to_email = to_email
        self.cc_email = cc_email
        self.subject = subject
        self.body = body
        self.folder_id = folder_id
