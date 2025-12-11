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

@router.get("/", name="home")
async def home(request: Request,current_user: dict = Depends(get_current_user), svc: AuthService = Depends(auth_service)):

    tpl = request.app.state.templates
    
    return tpl.TemplateResponse(
        "base.html",
        {"request": request, "title": "Webová aplikace"},
    )
    
@router.get("/new_user", name="home")
async def new_u(request: Request):
    mail="admin@admin.cz"
    full_name="Jan Turčínek"
    heslo="heslo321"
    ok=create_user(mail,full_name,hash_password(heslo))
    print(ok)

    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "base.html",
        {"request": request, "title": "Vložen uživatel"},
    )    
    
        
@router.get("/profile")
async def profile(request: Request, svc: AuthService = Depends(auth_service),current_user: dict = Depends(get_current_user)):
    tpl = request.app.state.templates
    data=svc.user_data(id=int(current_user["id"]))
    return tpl.TemplateResponse("profile.html", {"request": request, "user": data})



@router.get("/auth")
async def users(request: Request, svc: AuthService = Depends(auth_service),current_user: dict = Depends(get_current_user)):
    tpl = request.app.state.templates
    data=svc.user_data(id=int(current_user["id"]))
    print(data)
    return tpl.TemplateResponse("auth.html", {"request": request, "user":data})


@router.get("/users")
async def users(request: Request, svc: AuthService = Depends(auth_service),current_user: dict = Depends(get_current_user)):
    tpl = request.app.state.templates
    uzivatele=svc.get_user_list()
    return tpl.TemplateResponse("users.html", {"request": request,"user":current_user ,"users": uzivatele})




@router.post("/users")
async def new_user(
    request: Request,
    username: str = Form(...),
    full_name: str =Form(...),
    password: str = Form(...),
    svc: AuthService = Depends(auth_service),
):
    try:
        stav=svc.pridej_uzivatele(username,full_name,password)
        if "chyba" in stav:
            return tpl.TemplateResponse(
            "users.html",
            {"request": request, "error": stav["chyba"]},
            status_code=401,
                )
        else:
            return RedirectResponse(url="/users", status_code=303)
            
            
        return resp
    except Exception as e:
        print("LOGIN ERROR:", e)

@router.post("/user_change")
async def edit_user(
    request: Request,
    # tlačítka / volby z formuláře – volitelné:
    uprav_uzivatele: Annotated[int | None, Form(...)] = None,
    pridej_roli:     Annotated[int | None, Form(...)] = None,
    zmen_heslo:      Annotated[int | None, Form(...)] = None,
    # textová pole – volitelná:
    full_name: Annotated[str | None, Form(...)] = None,
    password:  Annotated[str | None, Form(...)] = None,
    # pozor: role přijde jako string, Pydantic ji převede na int
    role:      Annotated[int | None, Form(...)] = None,
    # povinné pole z formuláře:
    uziv:      Annotated[int, Form(...)] = None,
    # závislosti:
    svc:  AuthService = Depends(auth_service),
    current_user:  dict= Depends(get_current_user),
):

    if uprav_uzivatele==1:
       svc.set_new_user_full_name(full_name=full_name, id=uziv)
    if pridej_roli==1:
       print(role,uziv)
       svc.add_new_role(role,uziv)
    zmeneno=0
    if zmen_heslo==1:
       zmeneno=svc.set_new_password(password,uziv)
    
    uzivatel=svc.user_data(uziv)
    role=svc.get_role_list()
    user_roles=svc.get_user_roles_list(uziv)
    tpl = request.app.state.templates
    return tpl.TemplateResponse("user_detail.html", {"request": request, "data":uzivatel,"user": current_user,"user_roles": user_roles,"role":role,"heslo_zmeneno": zmeneno})
  
  
@router.post("/delete_role")
async def delete_role(
    request: Request,
    user_role_id: int = Form(...),
    uziv: int = Form(...),
    svc: AuthService = Depends(auth_service)
    ):
    svc.odstran_pravo(user_role_id)
    from urllib.parse import urlencode
    # Data, která chceme předat
    data_k_predani = {
        "uziv": uziv 
    }
    # Cílová URL bez parametrů
    base_url = "/user_change"
    # Sestavte query string: "user_id=12345&status=success"
    query_params = urlencode(data_k_predani)
    final_url = f"{base_url}?{query_params}"
    return RedirectResponse(url=final_url, status_code=307 )
            



