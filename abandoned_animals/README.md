# 🐾 유기동물 인스타그램 자동 포스팅 시스템

국가동물보호정보시스템 API를 활용하여 매일 자동으로 유기동물 정보를 수집하고 인스타그램 피드용 이미지를 생성하는 시스템입니다.

## 📋 목차

- [기능](#기능)
- [설치](#설치)
- [사용법](#사용법)
- [GitHub Actions 설정](#github-actions-설정)
- [API 정보](#api-정보)
- [파일 구조](#파일-구조)

## ✨ 기능

- 🔄 **자동 데이터 수집**: 공공데이터포털 API를 통해 최신 유기동물 정보 수집
- 🖼️ **이미지 자동 생성**: 5마리의 동물 정보를 담은 인스타그램 피드 이미지 생성
- 📸 **인스타그램 자동 포스팅**: 생성된 이미지를 인스타그램에 직접 업로드
- ⏰ **완전 자동화**: GitHub Actions를 통한 매일 자동 실행 (데이터 수집 → 이미지 생성 → 포스팅)
- 📊 **데이터 관리**: JSON 형식으로 데이터 보관 및 이력 관리

## 🚀 설치

### 필수 요구사항

- Python 3.11 이상
- pip (Python 패키지 관리자)
- 공공데이터포털 API 인증키

### 로컬 설치

1. 저장소 클론
```bash
git clone <repository-url>
cd FindYou-Data/abandoned_animals
```

2. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경변수 설정 (선택사항)
```bash
export ANIMAL_API_KEY="your_api_key_here"
```

## 📖 사용법

### 1. 동물 데이터 수집

```bash
python fetch_animals.py
```

이 스크립트는:
- 공공데이터포털 API에서 최신 공고 동물 5마리 정보를 가져옵니다
- 데이터를 `data/YYYY-MM-DD/animals.json` 형식으로 저장합니다
- 콘솔에 수집된 동물 정보를 출력합니다

**출력 예시:**
```
총 5마리의 동물 정보를 가져왔습니다:
1. 믹스견 - 발견장소: 세종시 금남면 - 공고번호: 세종-세종-2025-00375
2. 말티즈 - 발견장소: 진해구 자은동 - 공고번호: 경남-창원1-2025-00783
...
```

### 2. 인스타그램 피드 이미지 생성

```bash
python create_instagram_post.py
```

이 스크립트는:
- 오늘 날짜의 `animals.json` 파일을 읽습니다
- 5마리의 동물 정보와 이미지를 포함한 피드 이미지를 생성합니다
- 이미지를 `output/YYYY-MM-DD/instagram_post.png`로 저장합니다

**이미지 사양:**
- 크기: 1080 x 1350 픽셀 (Instagram 4:5 비율)
- 포맷: PNG
- 포함 정보: 동물 사진, 품종, 공고번호

### 3. 전체 프로세스 한번에 실행

```bash
# 데이터 수집
python fetch_animals.py

# 이미지 생성
python create_instagram_post.py
```

## ⚙️ GitHub Actions 설정

### 1. GitHub Secrets 설정

저장소의 Settings > Secrets and variables > Actions에서 다음 Secret을 추가하세요:

- **Name**: `ANIMAL_API_KEY`
- **Value**: 공공데이터포털에서 발급받은 API 인증키

### 2. 워크플로우 동작

`.github/workflows/daily_animal_post.yml` 파일이 다음 작업을 수행합니다:

- **자동 실행**: 매일 오전 9시 (KST) / 자정 (UTC)
- **수동 실행**: Actions 탭에서 "Run workflow" 버튼으로 즉시 실행 가능

**워크플로우 단계:**
1. ✅ 저장소 체크아웃
2. 🐍 Python 환경 설정
3. 📦 의존성 패키지 설치
4. 🔍 동물 데이터 수집
5. 🖼️ 인스타그램 이미지 생성
6. 📤 결과물 아티팩트로 업로드
7. 💾 데이터 및 이미지 커밋 & 푸시

### 3. 결과물 확인

- **Actions 탭**: 워크플로우 실행 기록 확인
- **Artifacts**: 생성된 이미지 다운로드 가능 (30일 보관)
- **저장소**: `abandoned_animals/output/` 디렉토리에 이미지 자동 커밋

## 🔑 API 정보

### 공공데이터포털 API

- **API 이름**: 농림축산식품부 농림축산검역본부_국가동물보호정보시스템 구조동물 조회 서비스
- **API URL**: https://www.data.go.kr/data/15098931/openapi.do
- **문서**: [공공데이터포털](https://www.data.go.kr/data/15098931/openapi.do)

### API 키 발급 방법

1. [공공데이터포털](https://www.data.go.kr) 회원가입 및 로그인
2. "국가동물보호정보시스템 구조동물 조회 서비스" 검색
3. "활용신청" 클릭
4. 자동 승인 후 "마이페이지 > 인증키 발급현황"에서 확인

### API 제한사항

- **개발 계정**: 일일 10,000회 호출
- **운영 계정**: 활용사례 등록 후 트래픽 증가 가능

## 📁 파일 구조

```
abandoned_animals/
├── fetch_animals.py              # 동물 데이터 수집 스크립트
├── create_instagram_post.py      # 인스타그램 이미지 생성 스크립트
├── requirements.txt              # Python 패키지 의존성
├── .gitignore                    # Git 제외 파일 설정
├── README.md                     # 프로젝트 문서
│
├── data/                         # 수집된 데이터 저장 (자동 생성)
│   └── YYYY-MM-DD/
│       └── animals.json          # 동물 데이터
│
└── output/                       # 생성된 이미지 저장 (자동 생성)
    └── YYYY-MM-DD/
        └── instagram_post.png    # 피드 이미지
```

## 🛠️ 클래스 및 주요 함수

### `AnimalDataFetcher` 클래스

동물 데이터를 수집하는 클래스입니다.

**주요 메서드:**
- `fetch_abandoned_animals()`: API를 호출하여 유기동물 정보 조회
- `get_recent_animals(count)`: 최신 공고 동물 N마리 데이터 가져오기
- `save_to_json(data, filepath)`: 데이터를 JSON 파일로 저장

### `InstagramPostCreator` 클래스

인스타그램 피드 이미지를 생성하는 클래스입니다.

**주요 메서드:**
- `download_image(url)`: URL에서 동물 이미지 다운로드
- `create_single_animal_card()`: 개별 동물 카드 생성
- `create_simple_grid(animals)`: 5마리 동물을 그리드 형태로 배치한 피드 생성

## 📝 예시 코드

### Python에서 사용하기

```python
from fetch_animals import AnimalDataFetcher
from create_instagram_post import InstagramPostCreator

# 데이터 수집
api_key = "your_api_key_here"
fetcher = AnimalDataFetcher(api_key)
animals = fetcher.get_recent_animals(count=5)

# 이미지 생성
creator = InstagramPostCreator()
feed_image = creator.create_simple_grid(animals)
feed_image.save("output.png")
```

## 🔧 커스터마이징

### 이미지 스타일 변경

`create_instagram_post.py`의 `InstagramPostCreator` 클래스에서:

```python
def __init__(self, width: int = 1080, height: int = 1350):
    self.width = width
    self.height = height
    self.background_color = (255, 255, 255)  # 배경색 변경
    self.text_color = (50, 50, 50)           # 텍스트 색상 변경
    self.accent_color = (255, 107, 107)      # 강조색 변경
```

### 동물 수 변경

`fetch_animals.py`의 `main()` 함수에서:

```python
# 5마리 대신 10마리 가져오기
animals = fetcher.get_recent_animals(count=10)
```

### 스케줄 변경

`.github/workflows/daily_animal_post.yml`에서:

```yaml
on:
  schedule:
    # 매일 오후 3시 (KST) = 오전 6시 (UTC)
    - cron: '0 6 * * *'
```

## 🐛 문제 해결

### API 호출 실패

- API 키가 올바른지 확인하세요
- 일일 호출 한도를 초과했는지 확인하세요
- 네트워크 연결 상태를 확인하세요

### 이미지 생성 실패

- `data/` 디렉토리에 오늘 날짜의 `animals.json` 파일이 있는지 확인하세요
- Pillow 패키지가 제대로 설치되었는지 확인하세요
- 동물 이미지 URL이 유효한지 확인하세요 (일부 이미지는 다운로드에 실패할 수 있습니다)

### GitHub Actions 실패

- Repository Secrets에 `ANIMAL_API_KEY`가 등록되어 있는지 확인하세요
- Actions 탭에서 에러 로그를 확인하세요
- 워크플로우 파일의 경로가 올바른지 확인하세요 (`.github/workflows/`)

## 📧 문의

문제가 발생하거나 제안사항이 있으시면 이슈를 등록해주세요.

## 📄 라이선스

이 프로젝트는 공공데이터를 활용하며, 공공데이터포털의 이용약관을 준수합니다.

## 🙏 크레딧

- 데이터 제공: 농림축산식품부 농림축산검역본부
- API: 공공데이터포털 (https://www.data.go.kr)
- 국가동물보호정보시스템: https://www.animal.go.kr

---

**🐶 🐱 소중한 생명들이 새로운 가족을 만나길 바랍니다! 🏠 ❤️**

