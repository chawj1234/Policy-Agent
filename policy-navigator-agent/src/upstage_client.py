import json
from typing import Dict

import requests

from config import MOCK_MODE, SOLAR_MODEL, UPSTAGE_API_KEY, UPSTAGE_BASE_URL


SOLAR_PATH = "/v1/solar"  # TODO: Upstage 문서에 맞춰 수정
DOCUMENT_PARSE_PATH = "/v1/document-parse"  # TODO: Upstage 문서에 맞춰 수정
INFORMATION_EXTRACT_PATH = "/v1/information-extract"  # TODO: Upstage 문서에 맞춰 수정


MOCK_SOLAR_RESPONSE = """
[판단 요약]
- 현재 프로필 기준으로 청년 주거·취업 지원 패키지 일부 항목에 해당 가능성이 높음
- 소득 기준과 거주 요건 증빙이 핵심

[선택지]
1) 월세 지원(12개월)
2) 직무교육 바우처(1회)
3) 구직활동비(6개월)

[시뮬레이션]
- 월세 지원 선택 시: 월 20만원 x 12개월 = 240만원 절감
- 구직활동비 선택 시: 월 10만원 x 6개월 = 60만원 확보

[추천 행동]
- 정부24 회원가입 및 본인인증 완료
- 주민등록등본, 소득증빙 서류 사전 발급
- 교육 바우처 과정 리스트 확인 후 1순위 선택

[추가 질문]
- 최근 3개월 소득 변동이 있나요?
- 현재 거주 형태(월세/전세/자가)는 무엇인가요?
""".strip()


MOCK_PARSED_DOC = {
    "text": "정책 문서 텍스트(파싱 결과) 예시",
    "pages": 3,
    "source": "mock",
}


MOCK_EXTRACTED_INFO = {
    "target": "만 19~34세, 수도권 거주, 중위소득 150% 이하, 미혼",
    "benefits": [
        "월세 지원: 월 20만원, 최대 12개월",
        "직무교육 바우처: 1회 50만원",
        "구직활동비: 월 10만원, 최대 6개월",
    ],
    "documents": [
        "주민등록등본",
        "소득증빙",
        "재직 또는 구직 확인서",
    ],
    "notes": "중복 수혜 제한, 허위 서류 제출 시 환수",
}


def _headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json",
    }


def call_solar(prompt: str) -> str:
    if MOCK_MODE:
        return MOCK_SOLAR_RESPONSE

    url = f"{UPSTAGE_BASE_URL}{SOLAR_PATH}"
    payload = {
        "model": SOLAR_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    # TODO: Upstage 문서에 맞춰 수정
    response = requests.post(url, headers=_headers(), json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    # TODO: Upstage 문서에 맞춰 수정
    return data.get("choices", [{}])[0].get("message", {}).get("content", "")


def call_document_parse(pdf_path: str) -> dict:
    if MOCK_MODE:
        parsed = dict(MOCK_PARSED_DOC)
        parsed["source"] = pdf_path
        return parsed

    url = f"{UPSTAGE_BASE_URL}{DOCUMENT_PARSE_PATH}"
    # TODO: Upstage 문서에 맞춰 수정
    with open(pdf_path, "rb") as file_handle:
        files = {"file": file_handle}
        response = requests.post(url, headers={"Authorization": f"Bearer {UPSTAGE_API_KEY}"}, files=files, timeout=60)
    response.raise_for_status()
    return response.json()


def call_information_extract(parsed_doc: dict) -> dict:
    if MOCK_MODE:
        return dict(MOCK_EXTRACTED_INFO)

    url = f"{UPSTAGE_BASE_URL}{INFORMATION_EXTRACT_PATH}"
    payload = {"document": parsed_doc}
    # TODO: Upstage 문서에 맞춰 수정
    response = requests.post(url, headers=_headers(), json=payload, timeout=60)
    response.raise_for_status()
    return response.json()
