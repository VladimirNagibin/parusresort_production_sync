from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.logger import logger
from core.settings import settings

test_router = APIRouter()
templates = Jinja2Templates(directory=f"{settings.BASE_DIR}/templates")


@test_router.get(
    "/",
    summary="check",
    description="Information about.",
)  # type: ignore
async def check(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})
