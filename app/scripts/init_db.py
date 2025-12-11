from app.models.db import open_conn

DDL = """
CREATE TABLE IF NOT EXISTS items(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nazev TEXT NOT NULL,
  popis TEXT,
  cena REAL NOT NULL
);
"""

if __name__ == "__main__":
    with open_conn() as c:
        c.executescript(DDL)
        c.commit()
        print("DB inicializována.")
