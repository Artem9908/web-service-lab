from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.invoice_service import generate_invoice


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "invoice_template.xlsx"
OUTPUT_DIR = BASE_DIR / "output"

app = FastAPI(title="Invoice Excel Service")


class InvoiceRequest(BaseModel):
    date: str = Field(description="Дата счета в формате YYYY-MM-DD")
    invoice_number: int = Field(description="Номер счета")
    period: str = Field(description="Период отображения в шапке")
    data: list[list[str]] = Field(description="Строки счета: 6 полей в каждой строке")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoice")
def create_invoice(payload: InvoiceRequest) -> FileResponse:
    try:
        generated_file = generate_invoice(
            template_path=TEMPLATE_PATH,
            output_dir=OUTPUT_DIR,
            date_iso=payload.date,
            invoice_number=payload.invoice_number,
            period=payload.period,
            data_rows=payload.data,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return FileResponse(
        path=generated_file,
        filename=generated_file.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
