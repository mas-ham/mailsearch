CREATE TABLE IF NOT EXISTS tr_mail_messages(
  sender TEXT,
  received TEXT,
  subject TEXT,
  body TEXT,
  folder_path TEXT,
  PRIMARY KEY (sender, received, subject)
)
