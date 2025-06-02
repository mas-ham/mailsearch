CREATE TABLE IF NOT EXISTS tr_mail_messages(
  entry_id TEXT,
  store_id TEXT,
  received TEXT,
  sender TEXT,
  sender_name TEXT,
  to_email TEXT,
  cc_email TEXT,
  subject TEXT,
  body TEXT,
  folder_id INTEGER,
  PRIMARY KEY (entry_id, store_id)
)
