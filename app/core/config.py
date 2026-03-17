from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "invoice_template.xlsx"
OUTPUT_DIR = BASE_DIR / "output"
