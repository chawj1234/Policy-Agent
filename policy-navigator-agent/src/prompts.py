import json


SAMPLE_POLICY_TEXT = """
정책명: 청년 주거·취업 지원 패키지(가상 예시)
대상: 만 19~34세, 수도권 거주, 중위소득 150% 이하, 미혼
내용:
- 월세 지원: 월 20만원, 최대 12개월
- 취업 역량 강화: 직무교육 바우처 1회 50만원
- 구직활동비: 월 10만원, 최대 6개월
신청 방법: 온라인 접수(정부24) 후 서류 제출
제출 서류: 주민등록등본, 소득증빙, 재직(또는 구직) 확인서
유의사항: 중복 수혜 제한, 허위 서류 제출 시 환수
""".strip()


SOLAR_PLANNER_TEMPLATE = """
역할: 당신은 정부 정책 문서를 개인 맞춤형 행동 가이드로 바꾸는 오케스트레이터다.
규칙:
- 요약 금지, 행동 중심, 피드백 루프 유지
- 판단/선택지/시뮬레이션/다음 행동/추가 질문을 포함
- 사용자의 상황을 기준으로 실제 실행 가능한 단계로 정리
- 아래 섹션 헤더를 반드시 포함

사용자 프로필:
{profile}

정책 원문:
{policy_text}

추출 정보(JSON):
{extracted_json}

출력 형식:
[판단 요약]
[선택지]
[시뮬레이션]
[추천 행동]
[추가 질문]
""".strip()


def build_solar_prompt(profile: str, policy_text: str, extracted_info: dict) -> str:
    extracted_json = json.dumps(extracted_info, ensure_ascii=False, indent=2)
    return SOLAR_PLANNER_TEMPLATE.format(
        profile=profile,
        policy_text=policy_text,
        extracted_json=extracted_json,
    )
