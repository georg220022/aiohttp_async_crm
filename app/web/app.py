# from urllib.request import Request
from typing import Optional
from aiohttp.web import (
    Application as AiohttpApplication,
    run_app as aiohttp_run_app,
    View as AiohttpView,
    Request as AiohttpRequest,
)
from app.store import setup_accessors
from app.store.crm.accessor import CrmAccessor
from app.web.config import Config, setup_config
from app.web.routes import setup_routes
from aiohttp_apispec import setup_aiohttp_apispec
from app.web.middlewares import setup_middlewares


class Application(AiohttpApplication):
    config: Optional[Config] = None
    database: dict = {}
    crm_accessor: Optional[CrmAccessor] = None


class Request(AiohttpRequest):
    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request


app = Application()


# Настройка приложения
def run_app():
    setup_config(app)  # Устанавливаем конфиги из yaml файла
    setup_routes(app)  # Устанавливаем роуты
    setup_aiohttp_apispec(
        app, title="Crm Application", url="/docs/json", swagger_path="/docs"
    )  # aiohttp api spec - валидация данных и генерация swagger
    setup_middlewares(app)  # Обрабатываем ошибки
    setup_accessors(app)  # CRM акцессор
    aiohttp_run_app(app)  # Запуск приложения
