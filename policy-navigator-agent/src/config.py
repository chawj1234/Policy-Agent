import os

from dotenv import load_dotenv


load_dotenv()


UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY", "")
UPSTAGE_BASE_URL = os.getenv("UPSTAGE_BASE_URL", "").rstrip("/")
SOLAR_MODEL = os.getenv("SOLAR_MODEL", "")

# 환경변수 필수 체크
if not UPSTAGE_API_KEY:
    raise ValueError("UPSTAGE_API_KEY 환경변수가 필요합니다.")
if not UPSTAGE_BASE_URL:
    raise ValueError("UPSTAGE_BASE_URL 환경변수가 필요합니다.")
if not SOLAR_MODEL:
    raise ValueError("SOLAR_MODEL 환경변수가 필요합니다.")
