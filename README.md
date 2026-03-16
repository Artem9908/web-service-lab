# Web Service Lab

Веб-сервис для тестового задания:
- принимает `POST` с данными счета;
- подставляет данные в Excel-шаблон;
- сохраняет копию в `output/`;
- отдает готовый `.xlsx` файлом в ответе.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoint

`POST /invoice`

Пример тела запроса:

```json
{
  "date": "2025-03-09",
  "invoice_number": 497,
  "period": "Февраль 2025",
  "data": [
    ["М-1", "76996700271", "0101251600157 КБ «ЭНЕРГОТРАНСБАНК» (АО)", "01.03.2025 - 31.03.2025", "2500", "2500,00"],
    ["М-3", "76996704602", "0101251600163 Тест ДФП", "10.03.2025 - 31.03.2025", "5000", "3548,38"]
  ]
}
```

Пример `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/invoice" \
  -H "Content-Type: application/json" \
  --data @payload.json \
  -o generated_invoice.xlsx
```

Шаблон используется из `templates/invoice_template.xlsx`.
