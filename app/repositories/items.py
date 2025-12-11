# app/repositories/items.py
from typing import List, Dict, Any, Optional
import sqlite3

def list_items(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows = conn.execute(
        "SELECT id, nazev, popis, cena FROM items ORDER BY id DESC"
    ).fetchall()
    return [dict(r) for r in rows]

def repo_prumer(conn: sqlite3.Connection) -> float:
    rows = conn.execute(
        "SELECT  avg(cena) prumer FROM items ORDER BY id DESC"
    ).fetchone()
    return rows["prumer"]

def repo_pocet(conn: sqlite3.Connection) -> float:
    rows = conn.execute(
        "SELECT  count(*) pocet FROM items ORDER BY id DESC"
    ).fetchone()
    return rows["pocet"]

def repo_max(conn: sqlite3.Connection) -> float:
    rows = conn.execute(
        "SELECT  max(cena) maximum FROM items ORDER BY id DESC"
    ).fetchone()
    return rows["maximum"]

def insert_item(
    conn: sqlite3.Connection,
    nazev: str,
    cena: float,
    popis: Optional[str] = None,
) -> int:
    cur = conn.execute(
        "INSERT INTO items(nazev, popis, cena) VALUES (?, ?, ?)",
        (nazev, popis, cena),
    )
    conn.commit()
    return cur.lastrowid
