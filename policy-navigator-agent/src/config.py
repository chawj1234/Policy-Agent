import os

from dotenv import load_dotenv


load_dotenv()


def _to_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY", "")
UPSTAGE_BASE_URL = os.getenv("UPSTAGE_BASE_URL", "").rstrip("/")
SOLAR_MODEL = os.getenv("SOLAR_MODEL", "")
MOCK_MODE = _to_bool(os.getenv("MOCK_MODE", "false"))

if not MOCK_MODE:
    if not UPSTAGE_API_KEY:
        raise ValueError("UPSTAGE_API_KEY is required when MOCK_MODE is false.")
    if not UPSTAGE_BASE_URL:
        raise ValueError("UPSTAGE_BASE_URL is required when MOCK_MODE is false.")
    if not SOLAR_MODEL:
        raise ValueError("SOLAR_MODEL is required when MOCK_MODE is false.")
