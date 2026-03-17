from datetime import date as DateType

from pydantic import BaseModel, Field, RootModel, field_validator


class InvoiceRow(RootModel[list[str]]):
    @field_validator("root")
    @classmethod
    def validate_row(cls, value: list[str]) -> list[str]:
        if len(value) != 6:
            raise ValueError("Каждая строка в data должна содержать 6 элементов")
        if any(not isinstance(item, str) or not item.strip() for item in value):
            raise ValueError("Все элементы строки data должны быть непустыми строками")
        return value


class InvoiceRequest(BaseModel):
    date: DateType = Field(description="Дата счета в формате YYYY-MM-DD")
    invoice_number: int = Field(gt=0, description="Номер счета")
    period: str = Field(min_length=1, description="Период отображения в шапке")
    data: list[InvoiceRow] = Field(min_length=1, description="Строки счета")

    @field_validator("period")
    @classmethod
    def validate_period(cls, value: str) -> str:
        period = value.strip()
        if not period:
            raise ValueError("Период не должен быть пустым")
        return period
