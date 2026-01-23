import json
import os
import re
from typing import Optional, Dict, Any

from config import MOCK_MODE
from prompts import SAMPLE_POLICY_TEXT, build_solar_prompt, build_plan_prompt
from upstage_client import call_document_parse, call_solar


REQUIRED_HEADERS = [
    "[판단 요약]",
    "[선택지]",
    "[시뮬레이션]",
    "[추천 행동]",
    "[추가 질문]",
]


DEFAULT_PLAN_RESULT = {
    "certain_conditions": ["만 19~34세", "수도권 거주"],
    "uncertain_conditions": ["중위소득 150% 이하", "미혼"],
    "questions": [
        {"field": "소득", "question": "최근 3개월 소득 변동이 있나요?"},
        {"field": "거주지", "question": "현재 거주 형태는 무엇인가요?"},
    ],
    "action_candidates": ["월세 지원", "직무교육 바우처", "구직활동비"],
}


def _ensure_required_headers(text: str) -> str:
    """Ensure the final output always contains the required section headers."""
    missing = [header for header in REQUIRED_HEADERS if header not in text]
    if not missing:
        return text.strip()

    lines = [text.strip()] if text.strip() else []
    for header in missing:
        lines.append(f"\n{header}\n- 내용이 생성되지 않았습니다. 입력/프롬프트를 확인해주세요.")
    return "\n".join(lines).strip()


def _policy_text_from_parsed_doc(parsed_doc: Dict[str, Any]) -> str:
    """Best-effort conversion of Document Parse response to a text blob for Solar."""
    # Upstage Document Parse commonly returns HTML when output_formats includes ["html"].
    for key in ("html", "text", "content"):
        val = parsed_doc.get(key)
        if isinstance(val, str) and val.strip():
            return val
        if isinstance(val, dict):
            for nested_key in ("html", "text"):
                nested_val = val.get(nested_key)
                if isinstance(nested_val, str) and nested_val.strip():
                    return nested_val

    # Sometimes responses include nested structures; fall back to JSON.
    try:
        return json.dumps(parsed_doc, ensure_ascii=False)[:20000]
    except Exception:
        return str(parsed_doc)[:20000]


def _default_plan_result() -> Dict[str, Any]:
    return dict(DEFAULT_PLAN_RESULT)


def _parse_plan_json(raw_text: str) -> Optional[Dict[str, Any]]:
    try:
        parsed = json.loads(raw_text)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        try:
            parsed = json.loads(raw_text[start : end + 1])
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None


def _plan_phase(profile: str, policy_text: str) -> Dict[str, Any]:
    if MOCK_MODE:
        return _default_plan_result()

    prompt = build_plan_prompt(profile=profile, policy_text=policy_text)
    output = call_solar(prompt)
    parsed = _parse_plan_json(output)
    return parsed if parsed else _default_plan_result()


def _append_profile_field(profile: str, field_name: str, value: str) -> str:
    updated_profile = profile.strip()
    if f"{field_name}:" in updated_profile:
        return updated_profile
    if updated_profile:
        return f"{updated_profile}/ {field_name}: {value}"
    return f"{field_name}: {value}"


def _update_profile_from_message(profile: str, user_message: str) -> str:
    updated_profile = profile.strip()

    age_match = re.search(r"(\d{2})\s*(세|살)", user_message)
    if age_match:
        updated_profile = _append_profile_field(updated_profile, "나이", f"{age_match.group(1)}세")

    income_match = re.search(r"월\s*(\d{2,4})\s*(만|만원)?", user_message)
    if income_match:
        updated_profile = _append_profile_field(updated_profile, "소득", f"월{income_match.group(1)}만원")

    if "미혼" in user_message:
        updated_profile = _append_profile_field(updated_profile, "혼인", "미혼")
    elif "기혼" in user_message:
        updated_profile = _append_profile_field(updated_profile, "혼인", "기혼")

    for location in ["수도권", "서울", "경기", "인천", "부산", "대구"]:
        if location in user_message:
            updated_profile = _append_profile_field(updated_profile, "거주지", location)
            break

    for job in ["중소기업", "대학생", "구직", "프리랜서", "직장인"]:
        if job in user_message:
            updated_profile = _append_profile_field(updated_profile, "직업", job)
            break

    return updated_profile


def run(profile: str, pdf_path: Optional[str] = None, interactive: bool = False) -> str:
    """Run the policy agent.

    - If `pdf_path` is provided: uses Document Parse to structure the PDF.
    - If not provided: uses embedded SAMPLE_POLICY_TEXT.
    - Information Extract는 사용하지 않습니다.
    """

    parsed_doc: Dict[str, Any]
    if pdf_path:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        parsed_doc = call_document_parse(pdf_path)
        policy_text = _policy_text_from_parsed_doc(parsed_doc)
    else:
        parsed_doc = {"source": "embedded", "text": SAMPLE_POLICY_TEXT}
        policy_text = SAMPLE_POLICY_TEXT

    plan_result = _plan_phase(profile=profile, policy_text=policy_text)
    answered_fields: Dict[str, str] = {}
    if interactive and plan_result.get("questions"):
        questions = plan_result.get("questions", [])
        print("\n추가 정보가 필요합니다:")
        for item in questions:
            if isinstance(item, dict):
                field_name = item.get("field")
                question_text = item.get("question") or field_name
            else:
                field_name = None
                question_text = str(item)

            if not question_text:
                continue

            answer = input(f"- {question_text}\n> ").strip()
            if not answer:
                continue

            if field_name:
                profile = _append_profile_field(profile, field_name, answer)
                answered_fields[field_name] = answer
            profile = _update_profile_from_message(profile, answer)

        plan_result = _plan_phase(profile=profile, policy_text=policy_text)

    plan_json = json.dumps(plan_result, ensure_ascii=False)
    answered_json = json.dumps(answered_fields, ensure_ascii=False) if answered_fields else None
    prompt = build_solar_prompt(
        profile=profile,
        policy_text=policy_text,
        agent_plan=plan_json,
        answered_fields=answered_json,
    )
    output = call_solar(prompt)

    return _ensure_required_headers(output)
