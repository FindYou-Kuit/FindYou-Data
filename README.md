# FindYou Data

FindU 프로젝트의 데이터 수집 및 관리 저장소입니다.

## 📁 프로젝트 구조

### 1. 품종 데이터 (`breed/`)
동물 품종 정보를 관리합니다.
- CSV, JSON 형식으로 저장
- 개, 고양이, 기타 동물 품종 정보

### 2. 시군구 데이터 (`sigungu/`)
대한민국 시도별 시군구 정보를 관리합니다.
- 지역별 JSON 파일
- CSV 통합 파일

### 3. 유기동물 데이터 (`abandoned_animals/`)
국가동물보호정보시스템 API를 활용한 유기동물 정보 수집 및 인스타그램 포스팅 자동화
- 매일 자동으로 최신 유기동물 정보 수집
- 인스타그램 피드용 이미지 자동 생성
- GitHub Actions를 통한 스케줄 실행

📖 자세한 내용은 [`abandoned_animals/README.md`](./abandoned_animals/README.md)를 참고하세요.

## 🚀 빠른 시작

### 유기동물 데이터 수집 및 포스팅

```bash
cd abandoned_animals
pip install -r requirements.txt
./run_daily.sh
```

## 📝 라이선스

공공데이터를 활용하며, 공공데이터포털의 이용약관을 준수합니다.