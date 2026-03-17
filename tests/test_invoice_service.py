from pathlib import Path

from openpyxl import load_workbook

from app.services.invoice_service import generate_invoice


def test_generate_invoice_with_many_rows(tmp_path: Path) -> None:
    data_rows = [
        [
            f"М-{index}",
            f"700000{index:05d}",
            f"ID {index}",
            "01.10.2025 - 31.10.2025",
            "1000",
            f"{1000 + index},00",
        ]
        for index in range(1, 13)
    ]

    output = generate_invoice(
        template_path=Path("templates/invoice_template.xlsx"),
        output_dir=tmp_path,
        date_iso="2025-10-31",
        invoice_number=1001,
        period="Октябрь 2025",
        data_rows=data_rows,
    )

    assert output.exists()
    workbook = load_workbook(output)
    sheet = workbook.active

    assert "Номер счета: 1001" in str(sheet["G1"].value)
    assert sheet["G2"].value == "Период: Октябрь 2025"
    assert sheet["A19"].value == "ИТОГО, руб. без учета НДС (20%)"
    assert sheet["A20"].value == "НДС (20%)"
    assert sheet["A21"].value == "ИТОГО, руб. с НДС (20%)"
    assert sheet["G19"].value > 0
    assert sheet["G20"].value > 0
    assert sheet["G21"].value > 0
