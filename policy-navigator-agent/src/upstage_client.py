import requests
from openai import OpenAI

from config import SOLAR_MODEL, UPSTAGE_API_KEY, UPSTAGE_BASE_URL


DOCUMENT_PARSE_PATH = "/document-digitization"


def _ensure_v1(base_url: str) -> str:
    """Upstage API는 /v1 경로가 필요함."""
    trimmed = base_url.rstrip("/")
    return trimmed if trimmed.endswith("/v1") else f"{trimmed}/v1"


VERSIONED_BASE_URL = _ensure_v1(UPSTAGE_BASE_URL)
SOLAR_BASE_URL = VERSIONED_BASE_URL


def call_solar(prompt: str) -> str:
    """Solar 모델을 호출하여 응답을 반환."""
    client = OpenAI(
        api_key=UPSTAGE_API_KEY,
        base_url=SOLAR_BASE_URL,
    )
    response = client.chat.completions.create(
        model=SOLAR_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=16384,
        stream=False,
    )
    return response.choices[0].message.content


def call_document_parse(pdf_path: str) -> dict:
    """Document Parse API를 호출하여 PDF를 파싱."""
    url = f"{VERSIONED_BASE_URL}{DOCUMENT_PARSE_PATH}"
    headers = {"Authorization": f"Bearer {UPSTAGE_API_KEY}"}
    data = {
        "model": "document-parse-nightly",
        "mode": "auto",
        "ocr": "auto",
        "chart_recognition": True,
        "coordinates": True,
        "output_formats": '["html"]',
        "base64_encoding": '["figure"]',
    }
    with open(pdf_path, "rb") as file_handle:
        files = {"document": file_handle}
        response = requests.post(url, headers=headers, files=files, data=data, timeout=120)
    response.raise_for_status()
    return response.json()
