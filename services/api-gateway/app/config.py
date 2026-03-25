import os


class Config:
    CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "").rstrip("/")
    REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "5"))
