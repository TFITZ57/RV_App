-- Core session & judging schema
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS session (
  id TEXT PRIMARY KEY,
  target_id TEXT NOT NULL,
  start_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
  end_ts DATETIME,
  mode TEXT CHECK(mode IN ('train','test')) DEFAULT 'train',
  stage_plan TEXT
);

CREATE TABLE IF NOT EXISTS target_truth (
  target_id TEXT PRIMARY KEY,
  target_path TEXT NOT NULL,
  sha256 TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transcript_page (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  stage TEXT,
  content TEXT,
  aol TEXT,
  ai TEXT,
  created_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES session(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sketch (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  stage TEXT,
  path TEXT NOT NULL,
  created_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES session(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS judging_pool (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  candidate_path TEXT NOT NULL,
  is_true INTEGER DEFAULT 0,
  FOREIGN KEY(session_id) REFERENCES session(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS judging_result (
  judge_run_id TEXT,
  session_id TEXT NOT NULL,
  candidate_path TEXT NOT NULL,
  rank INTEGER NOT NULL,
  is_true INTEGER DEFAULT 0,
  PRIMARY KEY (judge_run_id, candidate_path),
  FOREIGN KEY(session_id) REFERENCES session(id) ON DELETE CASCADE
);
