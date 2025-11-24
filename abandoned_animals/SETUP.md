# 🔧 설치 및 설정 가이드

## GitHub Actions 설정 (자동화)

### 1단계: API 키 등록

1. GitHub 저장소로 이동
2. **Settings** > **Secrets and variables** > **Actions** 클릭
3. **New repository secret** 클릭
4. 다음 정보 입력:
   - **Name**: `ANIMAL_API_KEY`
   - **Secret**: 공공데이터포털에서 발급받은 API 인증키 입력
5. **Add secret** 클릭

### 2단계: 워크플로우 권한 설정

1. **Settings** > **Actions** > **General** 클릭
2. **Workflow permissions** 섹션에서:
   - ✅ "Read and write permissions" 선택
   - ✅ "Allow GitHub Actions to create and approve pull requests" 체크
3. **Save** 클릭

### 3단계: 워크플로우 실행 확인

1. **Actions** 탭으로 이동
2. "Daily Animal Instagram Post" 워크플로우 확인
3. **Run workflow** 버튼으로 수동 실행 가능
4. 매일 자동 실행: 오전 9시 (KST)

## 로컬 실행 설정

### 필수 요구사항

- Python 3.11 이상
- pip 또는 pip3

### 설치 방법

1. **저장소 클론**
```bash
git clone <repository-url>
cd FindYou-Data/abandoned_animals
```

2. **가상 환경 생성 (권장)**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

3. **패키지 설치**
```bash
pip install -r requirements.txt
```

4. **환경변수 설정 (선택사항)**
```bash
export ANIMAL_API_KEY="your_api_key_here"
```

### 실행 방법

#### 방법 1: 쉘 스크립트 사용 (macOS/Linux)
```bash
./run_daily.sh
```

#### 방법 2: 개별 스크립트 실행
```bash
# 1. 데이터 수집
python fetch_animals.py

# 2. 이미지 생성
python create_instagram_post.py
```

#### 방법 3: API 테스트
```bash
# API 연결 및 데이터 확인
python test_api.py

# API 디버깅
python debug_api.py
```

## API 키 발급 방법

### 1단계: 공공데이터포털 회원가입

1. [공공데이터포털](https://www.data.go.kr) 접속
2. 회원가입 (일반 회원 또는 간편 인증)
3. 로그인

### 2단계: API 활용 신청

1. 검색창에 "국가동물보호정보시스템" 입력
2. **"농림축산식품부 농림축산검역본부_국가동물보호정보시스템 구조동물 조회 서비스"** 클릭
3. **활용신청** 버튼 클릭
4. 필수 정보 입력:
   - 활용 목적: (예: 유기동물 정보 제공 서비스 개발)
   - 상세 기능: (예: 인스타그램을 통한 유기동물 입양 홍보)
5. **신청** 클릭 (자동 승인)

### 3단계: API 키 확인

1. **마이페이지** > **오픈API** > **인증키 발급현황** 클릭
2. 발급된 인증키 확인
3. **일반 인증키 (Encoding)** 사용

### API 키 사용 시 주의사항

- ⚠️ **일반 인증키 (Encoding)** 를 사용하세요
- ⚠️ API 키는 절대 공개 저장소에 직접 올리지 마세요
- ⚠️ GitHub Secrets에만 저장하세요

## 트러블슈팅

### 문제 1: API 500 에러

**증상:**
```
500 Server Error: Internal Server Error
```

**가능한 원인:**
1. API 키가 잘못되었거나 만료됨
2. API 서비스가 일시적으로 중단됨
3. 요청 파라미터가 잘못됨

**해결 방법:**
1. 공공데이터포털에서 API 키 재확인
2. API 키를 다시 발급받아 시도
3. 공공데이터포털 고객센터(1566-0025) 문의
4. 공공데이터포털 공지사항 확인

### 문제 2: 모듈을 찾을 수 없음

**증상:**
```
ModuleNotFoundError: No module named 'requests'
```

**해결 방법:**
```bash
pip install -r requirements.txt
```

가상 환경을 사용하는 경우:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 문제 3: 권한 오류 (실행 불가)

**증상:**
```
Permission denied: ./run_daily.sh
```

**해결 방법:**
```bash
chmod +x run_daily.sh
```

### 문제 4: 이미지 생성 실패

**증상:**
```
데이터 파일을 찾을 수 없습니다
```

**해결 방법:**
1. 먼저 `fetch_animals.py`를 실행하여 데이터 수집
2. `data/YYYY-MM-DD/animals.json` 파일이 생성되었는지 확인
3. 그 후 `create_instagram_post.py` 실행

### 문제 5: GitHub Actions 실패

**가능한 원인:**
- Secrets에 `ANIMAL_API_KEY`가 등록되지 않음
- Workflow 권한이 부족함

**해결 방법:**
1. Settings > Secrets and variables > Actions 확인
2. Settings > Actions > General > Workflow permissions 확인
3. Actions 탭에서 에러 로그 확인

## 스케줄 커스터마이징

### GitHub Actions 스케줄 변경

`.github/workflows/daily_animal_post.yml` 파일 수정:

```yaml
on:
  schedule:
    # 매일 오후 3시 (KST) = 오전 6시 (UTC)
    - cron: '0 6 * * *'
    
    # 매주 월요일 오전 9시 (KST) = 자정 (UTC)
    - cron: '0 0 * * 1'
    
    # 매일 오전 9시, 오후 6시 (KST)
    - cron: '0 0,9 * * *'
```

### Cron 표현식 참고

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 요일 (0-7, 0과 7은 일요일)
│ │ │ └─── 월 (1-12)
│ │ └───── 일 (1-31)
│ └─────── 시 (0-23) UTC 기준
└───────── 분 (0-59)
```

**예시:**
- `0 0 * * *` - 매일 자정 (UTC)
- `0 */6 * * *` - 6시간마다
- `0 0 * * 1` - 매주 월요일 자정
- `0 9 1 * *` - 매월 1일 오전 9시

## 데이터 구조

### animals.json 형식

```json
[
  {
    "desertionNo": "20251124001",
    "filename": "http://example.com/image.jpg",
    "happenDt": "20251124",
    "happenPlace": "서울시 강남구",
    "kindCd": "[개] 믹스견",
    "colorCd": "갈색",
    "age": "2023년생(추정)",
    "weight": "5(Kg)",
    "noticeNo": "서울-강남-2025-00001",
    "noticeSdt": "20251124",
    "noticeEdt": "20251204",
    "popfile": "http://example.com/image.jpg",
    "processState": "공고중",
    "sexCd": "M",
    "neuterYn": "N",
    "specialMark": "활발함, 사람을 좋아함",
    "careNm": "서울시 강남구 동물보호센터",
    "careTel": "02-1234-5678",
    "careAddr": "서울시 강남구",
    "orgNm": "강남구",
    "chargeNm": "홍길동",
    "officeTel": "02-1234-5678"
  }
]
```

## 문의

문제가 발생하면 다음을 확인하세요:

1. **로그 확인**: Actions 탭에서 실행 로그 확인
2. **API 상태**: 공공데이터포털 공지사항 확인
3. **이슈 등록**: GitHub Issues에 문제 상세히 기술

---

**추가 지원이 필요하면 이슈를 등록해주세요!** 🙏

