from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

def setup_error_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Když není uživatel přihlášen
        if exc.status_code == 401:
            # Pokud je to prohlížeč (HTML), pošli redirect na login
            if "text/html" in request.headers.get("accept", ""):
                return RedirectResponse(url="/login")
            # Jinak (např. API call z JS nebo Postmana)
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        # Všechny ostatní HTTP chyby
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
