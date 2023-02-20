import os

ROOT_DIR = os.path.dirname(os.path.dirname((__file__)))

AIDBOX_HOST = os.getenv("AIDBOX_HOST") or "localhost"
AIDBOX_PORT = os.getenv("AIDBOX_PORT") or 8888
AIDBOX_ADMIN_CLIENT_ID = os.getenv("AIDBOX_ADMIN_CLIENT_ID") or "client"
AIDBOX_ADMIN_CLIENT_SECRET = os.getenv("AIDBOX_ADMIN_CLIENT_PW") or "secret"
