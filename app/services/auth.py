# app/services/auth.py
from typing import List
from app.core.security import verify_password, create_access_token,hash_password
from app.repositories import users as repo_users
from app.repositories.users import get_user_data,get_by_email, create_user, get_user_list as user_list
from app.repositories.users import set_new_user_full_name as repo_set_new_user_full_name, set_new_password as repo_set_new_password
from app.repositories.roles import user_roles as repo_user_roles, get_roles_list as roles_list
from app.repositories.roles import assign_role, repo_odstran_pravo

class AuthService:
    def login(self, email: str, password: str) -> str:
        """
        Ověří uživatele podle e-mailu/hesla a vrátí JWT token.
        Vyhazuje ValueError při špatných údajích.
        """
        u = repo_users.get_by_email(email)
        if not u or not verify_password(password, u["password_hash"]):
            raise ValueError("Neplatné přihlášení")
        roles = repo_user_roles(u["id"])
        return create_access_token(sub=str(u["id"]), roles=[ x["role"] for x in roles])
    
    def user_data(self,id : int) -> dict:
        return get_user_data(id)
    
    def pridej_uzivatele(sefl, username: str,full_name: str,password: str):
        if not get_by_email(username):
            return create_user(username,full_name,hash_password(password))
        else:
            return {"chyba": "mail byl již použit u jiného uživatele"}
        
    def set_new_user_full_name(self, full_name: str, id: int):
        """
        Změna jména uživatele
        """
        repo_set_new_user_full_name(full_name, id)
    
    def set_new_password(self,password:str, id:int) -> int:
        """
        Změna jména uživatele
        """        
        return repo_set_new_password(hash_password(password), id)
        
    def add_new_role(self,role:int, id:int):
        """
        Změna jména uživatele
        """        
        assign_role(id,role)
    
    def get_user_list(self):
        """
        Vrátí seznam uživatelů
        """
        return user_list()
    
    def get_user_roles_list(self,id) -> List[dict] :
        """
        vrati seznam uzivatelovych roli
        """
        return repo_user_roles(id)
        
    
    def get_role_list(self):
        """
        Vrátí seznam rolí
        """
        return roles_list()
    def odstran_pravo(self,id):
        repo_odstran_pravo(id)
        
        
        