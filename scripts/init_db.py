import os

from backend.db import init_db

if __name__ == "__main__":
    schema = os.path.join("backend", "schema.sql")
    init_db(schema)
    print("DB initialized.")
