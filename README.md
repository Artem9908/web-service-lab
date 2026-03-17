# Web Service Lab

Production-ready веб-сервис:
- принимает `POST` с данными счета;
- подставляет данные в Excel-шаблон;
- сохраняет копию в `output/`;
- отдает готовый `.xlsx` файлом в ответе;
- покрыт тестами и CI-проверками.

## Архитектура

```text
app/
  api/         # роуты и обработка ошибок
  core/        # конфигурация и logging
  schemas/     # pydantic-схемы запроса
  services/    # бизнес-логика генерации excel
```

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Локальная проверка качества

```bash
pip install -r requirements-dev.txt
ruff check .
black --check .
mypy app tests
pytest -q
```

## Pre-commit

```bash
pre-commit install
pre-commit run --all-files
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
    {
      "order_id": "М-1",
      "service_id": "76996700271",
      "device_name": "0101251600157 КБ «ЭНЕРГОТРАНСБАНК» (АО)",
      "period": "01.03.2025 - 31.03.2025",
      "sum": "2500",
      "total_sum": "2500,00"
    },
    {
      "order_id": "М-3",
      "service_id": "76996704602",
      "device_name": "0101251600163 Тест ДФП",
      "period": "10.03.2025 - 31.03.2025",
      "sum": "5000",
      "total_sum": "3548,38"
    }
  ]
}
```

Также поддерживается legacy-формат строк `data` как массив из 6 элементов для обратной совместимости.
Для шаблонов строки таблицы (обычно 7-я строка) поддерживаются плейсхолдеры:
- `{{index}}`, `{{order_id}}`, `{{service_id}}`, `{{device_name}}`, `{{period}}`, `{{sum}}`, `{{total_sum}}`
- и legacy-алиасы из старых шаблонов: `{{data0}}`, `{{data1}}`, `{{data2}}`, `{{data3}}`, `{{data5}}`, `{{data7}}`, `{{data10}}`

Пример `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/invoice" \
  -H "Content-Type: application/json" \
  --data @payload.json \
  -o generated_invoice.xlsx
```

Шаблон используется из `templates/invoice_template.xlsx`.
Для текстовых подстановок в шаблоне поддерживаются плейсхолдеры:
- `{{invoice_date}}`
- `{{invoice_number}}`
- `{{period}}`

## Docker

```bash
cp .env.example .env
docker compose up --build -d
```

Сервис в `docker-compose.yml` называется `doc-builder`.

### ENV-порты

- Внутри контейнера приложение всегда слушает `80`.
- Снаружи используется `HTTP_PORT` из `.env`.
- По умолчанию: `HTTP_PORT=8080`, значит endpoint доступен на `http://127.0.0.1:8080`.

### Volumes

- `./templates:/app/templates:ro` — шаблоны Excel берутся с хоста (read-only).
- `./output:/app/output` — результаты генерации сохраняются на хосте.

### Проверка после запуска

```bash
docker compose ps
curl http://127.0.0.1:${HTTP_PORT}/health
```

### Проверка генерации файла через Docker

```bash
curl -X POST "http://127.0.0.1:${HTTP_PORT}/invoice" \
  -H "Content-Type: application/json" \
  --data @payload.json \
  -o generated_from_docker.xlsx
```

Скопированная сервисом версия файла сохраняется в `output/` (эта папка примонтирована из хоста).
