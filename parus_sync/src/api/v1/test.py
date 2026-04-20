from typing import Any, Optional

from fastapi import (
    APIRouter,
    Depends,
    # Form,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

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


# --- Вложенные модели ---
class Topic(BaseModel):
    topic_id: int
    title: str
    parent_id: int

class Visitor(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    number: Optional[str] = None
    description: Optional[str] = None
    social: dict[str, Any] = Field(default_factory=dict)
    chats_count: Optional[int] = 0

class Agent(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class Department(BaseModel):
    id: int
    name: str

class Geoip(BaseModel):
    region_code: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    organization: Optional[str] = None

class UtmJson(BaseModel):
    source: Optional[str] = None
    campaign: Optional[str] = None
    content: Optional[str] = None
    medium: Optional[str] = None
    term: Optional[str] = None

class Session(BaseModel):
    geoip: Optional[Geoip] = None
    utm: Optional[str] = None
    utm_json: Optional[UtmJson] = None
    ip_addr: Optional[str] = None
    user_agent: Optional[str] = None

class Page(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None

class Call(BaseModel):
    type: Optional[str] = None          # callback, outgoing, etc.
    phone: Optional[str] = None
    status: Optional[str] = None        # start, end, missed, etc.
    record_url: Optional[str] = None

# --- Основная модель входящего вебхука ---
class JivoWebhookPayload(BaseModel):
    event_name: str
    chat_id: int
    topic: Topic
    widget_id: str
    visitor: Visitor
    agent: Agent
    department: Department
    session: Session
    page: Page
    call: Call
    analytics: dict[str, Any] = Field(default_factory=dict)

# --- Endpoint ---
@test_router.post("/webhook/jivo")
async def jivo_webhook(payload: JivoWebhookPayload):
    """
    Принимает события от Jivo (например, завершение звонка).
    """
    try:
        # Здесь добавьте вашу бизнес-логику:
        # - поиск/создание лида/сделки в Битрикс24
        # - сохранение записи разговора
        # - уведомление менеджеров и т.д.
        logger.info(payload.model_dump_json())
        print(f"Получено событие: {payload.event_name} от чата {payload.chat_id}")
        print(f"Звонок от {payload.visitor.name} статус {payload.call.status}")

        # Пример ответа
        return {"status": "ok", "message": "Event processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
