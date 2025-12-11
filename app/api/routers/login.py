from typing import List, Dict, Any, Optional, Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status
from app.services.items import ItemsService
from app.api.dependencies import items_service  # viz níže – vložíme hned teď
from fastapi.responses import RedirectResponse
from app.services.auth import AuthService
from app.api.dependencies import get_current_user
from app.repositories.users import create_user
from app.core.security import hash_password

router = APIRouter()

def auth_service() -> AuthService: return AuthService()


@router.get("/logout")
async def login_submit(
    request: Request,
    svc: AuthService = Depends(auth_service)
    ):
    # smaž cookies; pokud posíláš token v Authorization headeru,
    # na klientu je potřeba ho zapomenout (frontend).
    resp = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    for name in ("access_token", "refresh_token"):
        resp.delete_cookie(name, path="/")
    return resp


    
@router.get("/login")
async def login_page(request: Request):
    tpl = request.app.state.templates
    return tpl.TemplateResponse("login.html", {"request": request})

def auth_service() -> AuthService: return AuthService()



@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    svc: AuthService = Depends(auth_service),
):
    try:
        token = svc.login(username, password)  # musí být str (JWT)
        if not isinstance(token, str) or "." not in token:
            # velmi jednoduchá kontrola formátu JWT
            raise ValueError("Login nevrátil platný JWT")

        resp = RedirectResponse(url="/auth", status_code=303)
        resp.set_cookie(
            "access_token",          # stejné jméno jako výše
            value=token,
            httponly=True,
            samesite="lax",
            secure=False,            # produkce: True (HTTPS)
            max_age=60 * 60,
            path="/",
        )
        return resp
    except Exception as e:
        print("LOGIN ERROR:", e)
        tpl = request.app.state.templates
        return tpl.TemplateResponse(
            "login.html",
            {"request": request, "error": "Neplatné přihlášení"},
            status_code=401,
        )