from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_invoice_success() -> None:
    response = client.post(
        "/invoice",
        json={
            "date": "2025-03-09",
            "invoice_number": 497,
            "period": "Февраль 2025",
            "data": [
                [
                    "М-1",
                    "76996700271",
                    "0101251600157 КБ «ЭНЕРГОТРАНСБАНК» (АО)",
                    "01.03.2025 - 31.03.2025",
                    "2500",
                    "2500,00",
                ]
            ],
        },
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert len(response.content) > 1000


def test_create_invoice_success_with_named_rows() -> None:
    response = client.post(
        "/invoice",
        json={
            "date": "2025-03-09",
            "invoice_number": 498,
            "period": "Февраль 2025",
            "data": [
                {
                    "order_id": "М-1",
                    "service_id": "76996700271",
                    "device_name": "0101251600157 КБ «ЭНЕРГОТРАНСБАНК» (АО)",
                    "period": "01.03.2025 - 31.03.2025",
                    "sum": "2500",
                    "total_sum": "2500,00",
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert len(response.content) > 1000


def test_create_invoice_validation_error() -> None:
    response = client.post(
        "/invoice",
        json={
            "date": "2025-03-09",
            "invoice_number": 497,
            "period": "Февраль 2025",
            "data": [["короткая", "строка"]],
        },
    )
    assert response.status_code == 422
