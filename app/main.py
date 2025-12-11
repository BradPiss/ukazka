# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.api.routers.items import router as items_router  
from app.api.routers.home import router as home_router
from app.api.routers.login import router as login_router 
from app.api.dependencies import items_service
from app.services.items import ItemsService
from app.errors import setup_error_handlers

def create_app() -> FastAPI:
    app = FastAPI(title="Mini FastAPI – Items")

    setup_error_handlers(app) # připojím řešení errorů
    
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.state.templates = Jinja2Templates(directory="app/templates")

    app.include_router(items_router, prefix="/items", tags=["items"])
    app.include_router(home_router, prefix="", tags=["home"])
    app.include_router(login_router, prefix="", tags=["login"])
    

    
    
    # DEBUG: vypiš zaregistrované cesty
    print("=== ROUTES ===")
    for r in app.routes:
        try:
            print(getattr(r, "methods", ""), getattr(r, "path", ""))
        except Exception:
            pass


    return app

app = create_app()


