# 데모 실행 가이드

## 🎯 Interactive 모드 (추천!)

### Interactive 모드로 실행
```bash
cd /Users/chawj/Documents/Upstage/Policy-Agent/policy-navigator-agent
source .venv/bin/activate
MOCK_MODE=true python src/main.py --profile "29세/수도권/중소기업/월250/미혼" --interactive
```

### PDF 파일과 함께 Interactive 모드
```bash
MOCK_MODE=true python src/main.py --profile "29세/수도권/중소기업/월250/미혼" --pdf data/sample_policy.pdf --interactive
```

**사용 방법:**
- 초기 프로필을 입력하면 첫 번째 상담 결과가 표시됩니다
- 질문이 여러 개면 **한 질문씩 입력**합니다
- 각 질문의 field 기준으로 `field: 답변`이 프로필에 추가됩니다
- 입력 후 1회 재평가가 진행됩니다

**입력 예시:**
```
추가 정보가 필요합니다:
- 현재 월 소득 250만원이 중위소득 150% 이하에 해당하는지 확인할 수 있나요?
> 네, 대략 250만원 정도입니다
- 현재 재직 중이신가요, 아니면 구직 활동 중이신가요?
> 구직 활동 중입니다
- 기존에 다른 주거·취업 지원 사업을 받고 계신가요?
> 다른 사업은 받지 않습니다
```

---

## 빠른 시작 (MOCK_MODE - API 키 불필요)

### 1. 프로젝트 디렉토리로 이동
```bash
cd /Users/chawj/Documents/Upstage/Policy-Agent/policy-navigator-agent
```

### 2. 가상환경 활성화
```bash
source .venv/bin/activate
```

### 3. 데모 실행 (기본 - 샘플 텍스트 사용)
```bash
MOCK_MODE=true python src/main.py --profile "29세/수도권/중소기업/월250/미혼"
```

### 4. 데모 실행 (PDF 파일 사용)
```bash
MOCK_MODE=true python src/main.py --profile "29세/수도권/중소기업/월250/미혼" --pdf data/sample_policy.pdf
```

---

## 실제 API 사용 (Upstage API 키 필요)

### 1. 프로젝트 디렉토리로 이동
```bash
cd /Users/chawj/Documents/Upstage/Policy-Agent/policy-navigator-agent
```

### 2. 가상환경 활성화
```bash
source .venv/bin/activate
```

### 3. .env 파일 확인 (이미 설정되어 있음)
```bash
cat .env
```

### 4. 실제 API로 실행
```bash
python src/main.py --profile "29세/수도권/중소기업/월250/미혼"
```

### 5. PDF 파일과 함께 실행
```bash
python src/main.py --profile "29세/수도권/중소기업/월250/미혼" --pdf data/sample_policy.pdf
```

---

## 프로필 예시

다양한 프로필로 테스트할 수 있습니다:

```bash
# 청년 프로필
MOCK_MODE=true python src/main.py --profile "29세/수도권/중소기업/월250/미혼"

# 대학생 프로필
MOCK_MODE=true python src/main.py --profile "22세/지방/대학생/월50/미혼"

# 취업준비생 프로필
MOCK_MODE=true python src/main.py --profile "28세/수도권/구직중/월0/미혼"
```

---

## 한 줄 명령어 (MOCK_MODE)

```bash
cd /Users/chawj/Documents/Upstage/Policy-Agent/policy-navigator-agent && source .venv/bin/activate && MOCK_MODE=true python src/main.py --profile "29세/수도권/중소기업/월250/미혼"
```

---

## 도움말 보기

```bash
python src/main.py --help
```
