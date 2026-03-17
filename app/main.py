from fastapi import FastAPI

from app.api.errors import register_exception_handlers
from app.api.routes.health import router as health_router
from app.api.routes.invoices import router as invoice_router
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="Invoice Excel Service", version="1.0.0")
    app.include_router(health_router, tags=["health"])
    app.include_router(invoice_router, tags=["invoice"])
    register_exception_handlers(app)
    return app


app = create_app()
