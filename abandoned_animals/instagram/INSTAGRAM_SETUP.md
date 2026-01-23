# 📸 인스타그램 자동 포스팅 설정 가이드

인스타그램에 자동으로 포스팅하기 위한 설정 방법입니다.

## 🔑 필요한 것들

1. **Facebook 개발자 계정**
2. **인스타그램 비즈니스 계정**
3. **Facebook 페이지** (인스타그램과 연결됨)
4. **Facebook 앱** (Instagram Graph API 사용)

## 📋 단계별 설정

### 1단계: 인스타그램 비즈니스 계정 준비

1. **인스타그램 앱**에서 계정을 **비즈니스 계정**으로 전환
2. **Facebook 페이지**와 연결
   - 인스타그램 설정 → 계정 → 페이지 및 프로필 → Facebook 페이지 연결

### 2단계: Facebook 개발자 앱 생성

1. **[Facebook 개발자 콘솔](https://developers.facebook.com/)** 접속
2. **앱 만들기** 클릭
3. **비즈니스** 유형 선택
4. 앱 이름: "FindYou Animal Poster" (예시)
5. 앱 생성 완료

### 3단계: Instagram Graph API 설정

1. **앱 대시보드**에서 **제품 추가**
2. **Instagram Graph API** 추가
3. **Instagram 기본 표시** 추가

### 4단계: 액세스 토큰 발급

#### 4-1. 단기 토큰 발급

1. **Graph API 탐색기** 접속: https://developers.facebook.com/tools/explorer/
2. 앱 선택
3. **권한 추가**:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
4. **액세스 토큰 생성**

#### 4-2. 장기 토큰으로 변환

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={앱-ID}&client_secret={앱-시크릿}&fb_exchange_token={단기-토큰}"
```

#### 4-3. 페이지 액세스 토큰 획득

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/me/accounts?access_token={장기-토큰}"
```

#### 4-4. 인스타그램 계정 ID 획득

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/{페이지-ID}?fields=instagram_business_account&access_token={페이지-토큰}"
```

### 5단계: GitHub Secrets 설정

GitHub 저장소에서 다음 Secrets를 추가하세요:

1. **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** 클릭하여 추가:

```
INSTAGRAM_ACCESS_TOKEN: {페이지-액세스-토큰}
INSTAGRAM_ACCOUNT_ID: {인스타그램-비즈니스-계정-ID}
```

## 🧪 테스트 방법

### 로컬 테스트

```bash
# 환경변수 설정
export ANIMAL_API_KEY="your_api_key"
export INSTAGRAM_ACCESS_TOKEN="your_instagram_token"
export INSTAGRAM_ACCOUNT_ID="your_instagram_account_id"

# 테스트 실행
cd abandoned_animals
python auto_post.py
```

### GitHub Actions 테스트

1. **Actions** 탭 이동
2. **"Daily Animal Instagram Post"** 선택
3. **"Run workflow"** 클릭
4. 실행 결과 확인

## 🔧 문제 해결

### 일반적인 오류들

#### 1. "Invalid OAuth access token"
- 액세스 토큰이 만료되었거나 잘못됨
- 새로운 토큰을 발급받아야 함

#### 2. "Insufficient permissions"
- 필요한 권한이 부족함
- `instagram_content_publish` 권한 확인

#### 3. "Instagram account not found"
- 계정 ID가 잘못됨
- 비즈니스 계정으로 전환되지 않음

#### 4. "Media upload failed"
- 이미지 크기나 형식 문제
- 네트워크 연결 문제

### 디버깅 방법

```bash
# API 키 확인
python check_api_key.py

# 인스타그램 토큰 테스트
curl -i -X GET "https://graph.facebook.com/v18.0/me?access_token={토큰}"

# 계정 ID 확인
curl -i -X GET "https://graph.facebook.com/v18.0/{계정ID}?access_token={토큰}"
```

## 📝 중요 참고사항

### 제한사항

1. **게시 빈도**: 하루 25개 포스트 제한
2. **이미지 요구사항**:
   - 최소 크기: 320px
   - 최대 크기: 8MB
   - 지원 형식: JPG, PNG
3. **캡션 길이**: 최대 2,200자

### 보안

- **액세스 토큰을 절대 공개하지 마세요**
- GitHub Secrets에만 저장
- 정기적으로 토큰 갱신 (60일마다)

### 모니터링

- GitHub Actions 로그에서 실행 상태 확인
- 인스타그램에서 포스트 확인
- 오류 발생 시 이메일 알림 설정 가능

## 🎯 완성된 자동화 플로우

```
매일 오전 9시 (KST)
        ↓
GitHub Actions 트리거
        ↓
1. 유기동물 데이터 수집
        ↓
2. 인스타그램 이미지 생성
        ↓
3. 인스타그램 자동 포스팅
        ↓
4. 데이터만 GitHub에 저장
        ↓
완료! 🎉
```

---

**🐾 이제 완전 자동화된 유기동물 인스타그램 포스팅 시스템이 완성됩니다!**

매일 자동으로 새로운 유기동물 정보를 수집하고, 예쁜 이미지를 만들어서 인스타그램에 포스팅해줍니다! ❤️
