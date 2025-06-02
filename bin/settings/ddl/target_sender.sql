CREATE TABLE IF NOT EXISTS target_sender(
  sender_id INTEGER PRIMARY KEY AUTOINCREMENT,
  email_address TEXT,
  display_name TEXT,
  is_display INTEGER,
  is_checked INTEGER
)
