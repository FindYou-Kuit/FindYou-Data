#!/bin/bash

# 유기동물 인스타그램 포스트 자동 생성 스크립트
# 사용법: ./run_daily.sh

echo "🐾 유기동물 데이터 수집 및 인스타그램 포스트 생성 시작..."
echo "----------------------------------------"

# 스크립트 디렉토리로 이동
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. 동물 데이터 수집
echo "📡 Step 1: 동물 데이터 수집 중..."
python3 fetch_animals.py

if [ $? -ne 0 ]; then
    echo "❌ 데이터 수집 실패!"
    exit 1
fi

echo "✅ 데이터 수집 완료"
echo ""

# 2. 인스타그램 포스트 이미지 생성
echo "🖼️  Step 2: 인스타그램 이미지 생성 중..."
python3 create_instagram_post.py

if [ $? -ne 0 ]; then
    echo "❌ 이미지 생성 실패!"
    exit 1
fi

echo "✅ 이미지 생성 완료"
echo ""

# 3. 결과 확인
TODAY=$(date +%Y-%m-%d)
DATA_FILE="data/$TODAY/animals.json"
IMAGE_FILE="output/$TODAY/instagram_post.png"

echo "----------------------------------------"
echo "📊 생성된 파일:"
echo "  - 데이터: $DATA_FILE"
echo "  - 이미지: $IMAGE_FILE"
echo ""

if [ -f "$IMAGE_FILE" ]; then
    echo "🎉 모든 작업이 성공적으로 완료되었습니다!"
    echo "생성된 이미지를 인스타그램에 업로드하세요."
    
    # macOS에서 이미지 열기
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🖼️  이미지를 미리보기로 엽니다..."
        open "$IMAGE_FILE"
    fi
else
    echo "⚠️  이미지 파일을 찾을 수 없습니다."
    exit 1
fi

