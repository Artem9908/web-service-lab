from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.core.config import OUTPUT_DIR, TEMPLATE_PATH
from app.schemas.invoice import InvoiceRequest
from app.services.invoice_service import generate_invoice

router = APIRouter()


@router.post("/invoice")
def create_invoice(payload: InvoiceRequest) -> FileResponse:
    generated_file = generate_invoice(
        template_path=TEMPLATE_PATH,
        output_dir=OUTPUT_DIR,
        date_iso=payload.date.isoformat(),
        invoice_number=payload.invoice_number,
        period=payload.period,
        data_rows=payload.normalized_data_rows(),
    )
    return FileResponse(
        path=generated_file,
        filename=generated_file.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
