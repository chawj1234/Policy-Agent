# ==================================================
# Imports
# ==================================================
from typing import Optional


# ==================================================
# Solar 1차 분석 템플릿 (Plan 단계 - 조건 판단, 질문 생성)
# ==================================================

SOLAR_PLAN_TEMPLATE = """
역할:
너는 정책 문서와 사용자 프로필을 분석해 **판단에 필요한 정보**를 구조화한다.
최종 답변을 만들지 말고, 반드시 JSON만 출력한다.

목표:
- 확실한 조건과 불확실한 조건을 분리한다
- 부족한 정보는 질문으로 정리한다
- 추천 행동 후보를 리스트업한다
- 이미 제공된 정보는 다시 묻지 않고, 프로필과 모순되는 질문을 만들지 않는다

사용자 프로필:
{profile}

정책 문서 내용:
{policy_text}

{ie_extract}

참고: 정보 추출 요약은 참고용이며, 누락되거나 불완전할 수 있다. 판단은 반드시 정책 문서 원문을 최우선 근거로 수행하라.

출력 형식 (JSON만 출력):
{{
  "certain_conditions": ["..."],
  "uncertain_conditions": ["..."],
  "questions": [
    {{"field": "나이", "question": "만 나이가 어떻게 되나요?"}},
    {{"field": "거주지", "question": "현재 거주 지역이 수도권인가요?"}}
  ],
  "action_candidates": ["..."]
}}
""".strip()


def build_plan_prompt(profile: str, policy_text: str, ie_extract: Optional[str] = None) -> str:
    """
    Build a plan prompt for Solar to output JSON-only planning metadata.
    """
    return SOLAR_PLAN_TEMPLATE.format(
        profile=profile,
        policy_text=policy_text,
        ie_extract=_format_ie_extract(ie_extract),
    )


# ==================================================
# Solar 2차 분석 템플릿 (Final 단계 - 최종 행동 가이드 생성)
# ==================================================

SOLAR_PLANNER_TEMPLATE = """
역할:
너는 정부 정책 문서를 읽고, 이를 개인의 상황에 맞는 **행동 가능한 선택지**로 변환하는 AI Agent 오케스트레이터다.
너의 목적은 정보를 설명하는 것이 아니라, 사용자가 **다음에 무엇을 해야 할지 결정하도록 돕는 것**이다.

핵심 원칙:
- 단순 요약 금지 (정책 나열, 설명 위주의 답변 금지)
- 행동 중심 사고 유지
- 판단 → 선택지 → 결과 예측 → 행동 → 피드백 질문의 흐름을 반드시 따른다
- 사용자의 현재 상황을 기준으로 현실적으로 실행 가능한 내용만 제안한다

출력 규칙:
- 아래 5개 섹션 헤더를 반드시 모두 포함한다
- 수치를 제시할 때는 정확한 최신 기준을 확인해야 한다고 말하고, 단정 수치 대신 '확인 필요'로 표현하라.
- [자격 판단]의 첫 문장에는 반드시 판단 대상이 되는 정책명을 명시하여, 사용자가 어떤 정책에 대한 설명인지 즉시 알 수 있도록 한다
- 각 섹션은 구체적이고 명확해야 하며, 추상적인 표현을 피한다
- 정보가 부족한 경우, 이를 숨기지 말고 [확인 필요 사항]에서 명확히 질문한다
- 사용자가 제공하지 않은 정보(가구원수, 연도 기준, 소득 판정 등)는 확정 표현(완전히 일치/확실) 대신 '가능성/확인 필요'로 표현하라.
- [확인 필요 사항]에는 아직 답을 모르는 정보만 포함하고, 이미 제공된 정보는 다시 묻지 않는다
- 오타/띄어쓰기 오류 없이 작성
- 정책명/지역명/용어는 원문 그대로 유지


사용자 프로필:
{profile}

정책 문서 내용:
{policy_text}

{ie_extract}

{agent_plan}

{answered_fields}

참고: 정보 추출 요약은 참고용이며, 누락되거나 불완전할 수 있다. 판단은 반드시 정책 문서 원문을 최우선 근거로 수행하라.

출력 형식 (형식 유지 필수):
[자격 판단]
- 사용자가 해당 정책의 자격 요건을 충족하는지 판단하고, 그 이유를 설명

[신청 가능 정책]
- 사용자가 신청할 수 있는 정책 목록을 2~3가지 제시

[예상 혜택]
- 각 정책을 신청할 경우 받을 수 있는 혜택을 구체적으로 비교

[다음 단계]
- 현재 사용자에게 가장 합리적인 행동을 단계별로 제시

[확인 필요 사항]
- 판단을 더 정확히 하기 위해 사용자가 확인해야 할 정보 (있을 경우)
""".strip()


def build_solar_prompt(
    profile: str,
    policy_text: str,
    agent_plan: Optional[str] = None,
    answered_fields: Optional[str] = None,
    ie_extract: Optional[str] = None,
) -> str:
    """
    Build a structured planner prompt for Solar.
    The prompt is designed to force agentic (plan-and-act) behavior,
    not summarization.
    """

    return SOLAR_PLANNER_TEMPLATE.format(
        profile=profile,
        policy_text=policy_text,
        ie_extract=_format_ie_extract(ie_extract),
        agent_plan=_format_agent_plan(agent_plan),
        answered_fields=_format_answered_fields(answered_fields),
    )


# ==================================================
# Helper Functions
# ==================================================

def _format_ie_extract(ie_extract: Optional[str]) -> str:
    if not ie_extract:
        return ""
    return f"정보 추출 요약(참고용):\n{ie_extract}"


def _format_agent_plan(agent_plan: Optional[str]) -> str:
    if not agent_plan:
        return ""
    return f"에이전트 계획 결과:\n{agent_plan}"


def _format_answered_fields(answered_fields: Optional[str]) -> str:
    if not answered_fields:
        return ""
    return f"이미 제공된 답변:\n{answered_fields}"
