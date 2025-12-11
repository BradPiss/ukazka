# app/services/items.py
from typing import List, Dict, Any, Optional
import sqlite3

# DŮLEŽITÉ: importuj přímo funkce – vyhneš se kolizím názvů
from app.repositories.items import list_items as repo_list_items, insert_item as repo_insert_item,repo_prumer,repo_pocet,repo_max

class ItemsService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_items(self) -> List[Dict[str, Any]]:
        return repo_list_items(self.conn)
    
    def drahe_vyrobky(self) -> List[Dict[str, Any]]:
        return [x for x in repo_list_items(self.conn) if x["cena"]>150]
    
    def statistika(self) -> Dict[str,Any]:
        return {"prumer":repo_prumer(self.conn),
                "pocet":repo_pocet(self.conn),
                "max":repo_max(self.conn)}

    def create_item(self, nazev: str, cena: float, popis: Optional[str] = None) -> int:
        return repo_insert_item(self.conn, nazev=nazev, cena=cena, popis=popis)
