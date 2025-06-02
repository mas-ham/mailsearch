CREATE TABLE IF NOT EXISTS target_folder(
  folder_id INTEGER PRIMARY KEY AUTOINCREMENT,
  folder_path TEXT,
  folder_type INTEGER,
  is_target INTEGER
)
