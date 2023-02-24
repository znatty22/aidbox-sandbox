import os

ROOT_DIR = os.path.dirname(os.path.dirname((__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

AIDBOX_HOST = os.getenv("AIDBOX_HOST") or "localhost"
AIDBOX_PORT = os.getenv("AIDBOX_PORT") or 8888
AIDBOX_ADMIN_CLIENT_ID = os.getenv("AIDBOX_ADMIN_CLIENT_ID") or "client"
AIDBOX_ADMIN_CLIENT_SECRET = os.getenv("AIDBOX_ADMIN_CLIENT_PW") or "secret"

BASE_URL = f"http://{AIDBOX_HOST}:{AIDBOX_PORT}"
FHIR_URL = f"{BASE_URL}/fhir"
