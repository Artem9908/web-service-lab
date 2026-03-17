from datetime import date as DateType

from pydantic import BaseModel, Field, RootModel, field_validator


class LegacyInvoiceRow(RootModel[list[str | int | float]]):
    @field_validator("root")
    @classmethod
    def validate_row(cls, value: list[str | int | float]) -> list[str | int | float]:
        if len(value) != 6:
            raise ValueError("Каждая строка в data должна содержать 6 элементов")
        if any(not str(item).strip() for item in value):
            raise ValueError("Все элементы строки data должны быть непустыми строками")
        return value

    def to_legacy_row(self) -> list[str]:
        return [str(item).strip() for item in self.root]


class InvoiceDataItem(BaseModel):
    order_id: str = Field(min_length=1, description="№ Заказа")
    service_id: str = Field(min_length=1, description="ТПО")
    device_name: str = Field(min_length=1, description="ID, наименование устройства")
    period: str = Field(min_length=1, description="Период услуги")
    sum: str | int | float = Field(description="Тариф, руб. без НДС")
    total_sum: str | int | float = Field(description="Стоимость за период, руб. без НДС")

    @field_validator("order_id", "service_id", "device_name", "period")
    @classmethod
    def validate_text_field(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Текстовые поля строки data должны быть непустыми")
        return normalized

    def to_legacy_row(self) -> list[str]:
        return [
            self.order_id,
            self.service_id,
            self.device_name,
            self.period,
            str(self.sum).strip(),
            str(self.total_sum).strip(),
        ]


class InvoiceRequest(BaseModel):
    date: DateType = Field(description="Дата счета в формате YYYY-MM-DD")
    invoice_number: int = Field(gt=0, description="Номер счета")
    period: str = Field(min_length=1, description="Период отображения в шапке")
    data: list[InvoiceDataItem | LegacyInvoiceRow] = Field(min_length=1, description="Строки счета")

    @field_validator("period")
    @classmethod
    def validate_period(cls, value: str) -> str:
        period = value.strip()
        if not period:
            raise ValueError("Период не должен быть пустым")
        return period

    def normalized_data_rows(self) -> list[list[str]]:
        normalized_rows: list[list[str]] = []
        for row in self.data:
            normalized_rows.append(row.to_legacy_row())
        return normalized_rows
