import os
from typing import Optional

from prompts import SAMPLE_POLICY_TEXT, build_solar_prompt
from upstage_client import call_document_parse, call_information_extract, call_solar


REQUIRED_HEADERS = [
    "[판단 요약]",
    "[선택지]",
    "[시뮬레이션]",
    "[추천 행동]",
    "[추가 질문]",
]


def _ensure_required_headers(text: str) -> str:
    missing = [header for header in REQUIRED_HEADERS if header not in text]
    if not missing:
        return text.strip()

    lines = [text.strip()] if text.strip() else []
    for header in missing:
        lines.append(f"\n{header}\n- 내용이 생성되지 않았습니다. 입력을 확인해주세요.")
    return "\n".join(lines).strip()


def run(profile: str, pdf_path: Optional[str] = None) -> str:
    if pdf_path:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        parsed_doc = call_document_parse(pdf_path)
        policy_text = parsed_doc.get("text", "")
    else:
        parsed_doc = {"text": SAMPLE_POLICY_TEXT, "source": "embedded"}
        policy_text = SAMPLE_POLICY_TEXT

    extracted_info = call_information_extract(parsed_doc)
    prompt = build_solar_prompt(profile, policy_text, extracted_info)
    output = call_solar(prompt)

    return _ensure_required_headers(output)
