from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status
from app.services.items import ItemsService
from app.api.dependencies import items_service  # viz níže – vložíme hned teď

router = APIRouter()


@router.get("/ui", name="items_ui")
async def items_ui(request: Request, svc: ItemsService = Depends(items_service)):
    items: List[Dict[str, Any]] = svc.list_items()
    total = sum(i["cena"] for i in items) if items else 0.0
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "items.html",
        {"request": request, "title": "Seznam položek", "items": items, "total": total},
    )
    
@router.get("/drahe", name="items_ui")
async def items_ui(request: Request, svc: ItemsService = Depends(items_service)):
    items: List[Dict[str, Any]] = svc.drahe_vyrobky()
    total = sum(i["cena"] for i in items) if items else 0.0
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "items.html",
        {"request": request, "title": "Seznam položek", "items": items, "total": total},
    )    

@router.get("/statistiky", name="items_ui")
async def items_ui(request: Request, svc: ItemsService = Depends(items_service)):
    statistika: List[Dict[str, Any]] = svc.statistika()
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "statistika.html",
        {"request": request, "title": "Statistiky", "stat": statistika},
    )   


@router.post("/ui", name="items_ui_post")
async def items_ui_post(
    request: Request,
    nazev: str = Form(...),
    cena: float = Form(...),
    popis: Optional[str] = Form(None),
    svc: ItemsService = Depends(items_service),
):
    svc.create_item(nazev=nazev, cena=cena, popis=popis)
    return RedirectResponse(url=request.url_for("items_ui"), status_code=status.HTTP_303_SEE_OTHER)
