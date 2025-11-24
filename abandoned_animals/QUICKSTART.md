# ⚡ 빠른 시작 가이드

5분 안에 유기동물 인스타그램 포스트 자동화 시스템을 설정하세요!

## 📋 체크리스트

- [ ] Python 3.11 이상 설치됨
- [ ] 공공데이터포털 API 키 발급받음
- [ ] GitHub 저장소 있음

## 🚀 3단계로 시작하기

### 1️⃣ 로컬에서 테스트

```bash
# 1. 저장소로 이동
cd abandoned_animals

# 2. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. 패키지 설치
pip install -r requirements.txt

# 4. API 키 확인
python check_api_key.py

# 5. API 테스트
python test_api.py

# 6. 전체 실행 (데이터 수집 + 이미지 생성)
./run_daily.sh
```

### 2️⃣ GitHub Actions 설정

```bash
# 1. GitHub 저장소 Settings 이동
# 2. Secrets and variables > Actions 클릭
# 3. New repository secret 클릭
#    - Name: ANIMAL_API_KEY
#    - Secret: (여기에 API 키 붙여넣기)
# 4. Add secret 클릭
```

### 3️⃣ 자동화 활성화

```bash
# 1. Actions 탭 이동
# 2. "I understand my workflows, go ahead and enable them" 클릭
# 3. "Daily Animal Instagram Post" 선택
# 4. "Run workflow" 버튼으로 즉시 실행 테스트!
```

## 📁 생성되는 파일

실행 후 다음 파일들이 생성됩니다:

```
abandoned_animals/
├── data/
│   └── 2025-11-24/
│       └── animals.json          ← 수집된 동물 데이터
└── output/
    └── 2025-11-24/
        └── instagram_post.png    ← 인스타그램 업로드용 이미지
```

## 🎨 결과물

생성되는 인스타그램 이미지:
- **크기**: 1080 x 1350px (4:5 비율)
- **내용**: 5마리의 유기동물 정보
- **포함 정보**: 사진, 품종, 공고번호, 발견장소

## ⏰ 자동 실행 스케줄

- **기본 설정**: 매일 오전 9시 (한국 시간)
- **커스터마이징**: `.github/workflows/daily_animal_post.yml` 수정

## ❓ 문제 발생 시

### API 500 에러가 발생해요
```bash
# API 키 재확인
python check_api_key.py

# API 테스트
python test_api.py
```

**해결 방법:**
1. 공공데이터포털에서 활용신청 상태 확인
2. "일반 인증키 (Encoding)" 사용 확인
3. API 키 재발급 시도

### 이미지가 생성되지 않아요
```bash
# 데이터 파일 확인
ls -la data/$(date +%Y-%m-%d)/

# 데이터가 없다면 다시 수집
python fetch_animals.py

# 이미지 생성
python create_instagram_post.py
```

### GitHub Actions가 실패해요

**확인 사항:**
1. Secrets에 `ANIMAL_API_KEY` 등록되어 있나요?
2. Actions 권한이 "Read and write"로 설정되어 있나요?
3. Actions 탭에서 에러 로그를 확인하셨나요?

## 📚 더 알아보기

- **상세 문서**: [README.md](./README.md)
- **설정 가이드**: [SETUP.md](./SETUP.md)
- **API 문서**: [공공데이터포털](https://www.data.go.kr/data/15098931/openapi.do)

## 🎯 다음 단계

### 1. 인스타그램 업로드

```bash
# 생성된 이미지 위치
open output/$(date +%Y-%m-%d)/instagram_post.png
```

이미지를 다운로드하여 인스타그램에 업로드하세요!

### 2. 캡션 작성 예시

```
🐾 새로운 가족을 기다립니다

오늘도 5마리의 친구들이 여러분을 기다리고 있어요.
따뜻한 가정에서 사랑받을 권리가 있습니다.

❤️ 입양 문의는 각 공고번호로 해당 보호센터에 연락하세요.

#유기동물 #입양 #반려동물 #유기견 #유기묘 
#동물보호 #입양문의 #사지말고입양하세요
```

### 3. 자동화 완성

GitHub Actions가 매일 자동으로:
1. ✅ 최신 유기동물 정보 수집
2. ✅ 인스타그램 피드 이미지 생성
3. ✅ 저장소에 자동 커밋
4. ✅ Artifacts로 다운로드 가능

## 💡 팁

### 동물 수 변경하기

`fetch_animals.py` 파일에서:

```python
# 5마리 대신 10마리
animals = fetcher.get_recent_animals(count=10)
```

### 이미지 스타일 변경하기

`create_instagram_post.py` 파일에서:

```python
# 색상 변경
self.accent_color = (255, 107, 107)  # 빨강 계열
# → (107, 255, 107)  # 초록 계열
# → (107, 107, 255)  # 파랑 계열
```

### 실행 시간 변경하기

`.github/workflows/daily_animal_post.yml` 파일에서:

```yaml
schedule:
  # 오후 3시 (KST)로 변경
  - cron: '0 6 * * *'
```

## 🤝 기여하기

개선 아이디어가 있으신가요?
- 이슈 등록
- Pull Request 생성
- 피드백 공유

---

**🐶 🐱 소중한 생명들이 가족을 만나는 그날까지!** ❤️

