import sqlite3
from typing import Iterator
from fastapi import Depends, Request,Cookie
from fastapi.responses import RedirectResponse
from app.models.db import open_conn
from app.services.items import ItemsService
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
import jwt
from app.core.config import settings
from app.repositories import users as repo_users
from app.repositories.roles import user_roles as repo_user_roles

def get_conn() -> Iterator[sqlite3.Connection]:
    with open_conn() as conn:
        yield conn

def items_service(conn: sqlite3.Connection = Depends(get_conn)) -> ItemsService:
    return ItemsService(conn)


oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

def _extract_token(request: Request, bearer: str | None):
    # 1) Bearer z hlavičky, 2) fallback: cookie
    if bearer:
        return bearer
    cookie = request.cookies.get("access_token")
    print(cookie)
    return cookie   

ACCESS_COOKIE = "access_token"  # stejné jméno jako v set_cookie

def get_current_user(access_token: str | None = Cookie(default=None, alias=ACCESS_COOKIE)):
    if not access_token:
        return RedirectResponse(url="/login", status_code=303)
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing cookie")
    try:
        payload = decode_access_token(access_token)
    except ValueError as e:
        # z decode_access_token ("Token expiroval" / "Neplatný token")
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        return RedirectResponse(url="/login", status_code=303,method="get")
    return {"id": payload["sub"], "roles": payload.get("roles", [])}
    
    
async def require_admin(user: dict = Depends(get_current_user)):
    if "admin" not in user.get("roles", []):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Pouze pro adminy")
    return user