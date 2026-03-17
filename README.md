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
