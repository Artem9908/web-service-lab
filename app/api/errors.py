import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.invoice_service import InvoiceServiceError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvoiceServiceError)
    async def handle_invoice_service_error(_: Request, exc: InvoiceServiceError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
