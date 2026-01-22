# Policy Navigator Agent

## 프로젝트 개요
정부 정책 문서를 개인 맞춤형 행동 가이드로 변환하는 AI Agent 프로토타입입니다. 입력된 사용자 프로필과 정책 문서를 바탕으로 실행 가능한 행동 플랜과 추가 질문을 생성합니다.

## 왜 Agent인가
정책 문서는 조건과 예외가 많고, 사용자는 자신의 상황에 맞는 "다음 행동"이 필요합니다. Agent는 판단(조건 검증) → 계획(선택지 구성) → 검증(피드백 루프) 흐름을 통해 실제 신청 가능성 중심의 행동 가이드를 제공합니다.

## Agent 흐름 다이어그램(ASCII)
```
[입력 프로필/정책 문서]
          |
          v
[Document Parse] -> (필요 시)
          |
          v
[Information Extract]
          |
          v
[Upstage Solar 오케스트레이터]
          |
          v
[판단/선택지/시뮬레이션/추천 행동/추가 질문]
```

## Upstage 제품 역할 분리
- Solar: 오케스트레이터(판단/계획/검증), 최종 행동 가이드 생성
- Document Parse: PDF 문서 파싱(텍스트/구조 추출)
- Information Extract: 정책 요건/혜택/제출서류 등 핵심 정보 추출

## 데모 시나리오(20대 청년)
- 입력: "29세/수도권/중소기업/월250/미혼"
- 정책 문서: 청년 주거·취업 지원 패키지(샘플 텍스트 또는 PDF)
- 출력: 월세지원/직무교육/구직활동비 등 선택지와 신청 단계

## 실행 방법
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py --pdf data/sample_policy.pdf --profile "29세/수도권/중소기업/월250/미혼"
```

- PDF 파일이 없으면 `--pdf` 없이 실행 가능합니다.
- 이 경우 내장된 샘플 정책 텍스트를 사용합니다.

## MOCK_MODE 안내
- `.env`에서 `MOCK_MODE=true`로 설정하면 실제 API 호출 없이 데모가 동작합니다.
- API 키가 없어도 `python src/main.py --profile "29세/수도권/중소기업/월250/미혼"` 실행이 가능합니다.

## 교육 콘텐츠 확장 가능성
- 정책 문서를 과제/케이스 스터디로 변환
- 행동 가이드 기반 체크리스트/퀴즈 생성
- 개인 맞춤형 피드백 루프 설계
