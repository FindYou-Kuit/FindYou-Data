"""
API 연결 및 데이터 수집 테스트 스크립트
"""
import os
from fetch_animals import AnimalDataFetcher

def test_api_connection():
    """API 연결 테스트"""
    print("🔍 API 연결 테스트 시작...\n")
    
    # API 키 (환경변수 또는 기본값)
    api_key = os.getenv(
        'ANIMAL_API_KEY',
        'Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D'
    )
    
    fetcher = AnimalDataFetcher(api_key)
    
    # 1. 기본 API 호출 테스트
    print("1️⃣ 기본 API 호출 테스트")
    print("-" * 50)
    data = fetcher.fetch_abandoned_animals(num_of_rows=3, page_no=1)
    
    if not data:
        print("❌ API 호출 실패: 데이터를 받을 수 없습니다.")
        return False
    
    print("✅ API 호출 성공!")
    print(f"응답 키: {list(data.keys())}")
    
    if 'response' in data:
        response = data['response']
        print(f"Response 키: {list(response.keys())}")
        
        if 'header' in response:
            header = response['header']
            print(f"\n📋 헤더 정보:")
            print(f"  - 결과 코드: {header.get('resultCode', 'N/A')}")
            print(f"  - 결과 메시지: {header.get('resultMsg', 'N/A')}")
        
        if 'body' in response:
            body = response['body']
            print(f"\n📊 바디 정보:")
            print(f"  - 총 개수: {body.get('totalCount', 0)}")
            print(f"  - 페이지 번호: {body.get('pageNo', 'N/A')}")
            print(f"  - 페이지당 개수: {body.get('numOfRows', 'N/A')}")
    
    print("\n" + "=" * 50 + "\n")
    
    # 2. 동물 데이터 파싱 테스트
    print("2️⃣ 동물 데이터 파싱 테스트")
    print("-" * 50)
    animals = fetcher.get_recent_animals(count=5)
    
    if not animals:
        print("❌ 동물 데이터를 파싱할 수 없습니다.")
        return False
    
    print(f"✅ {len(animals)}마리의 동물 데이터를 파싱했습니다!\n")
    
    # 동물 정보 출력
    for i, animal in enumerate(animals, 1):
        print(f"🐾 동물 #{i}")
        print(f"  - 품종: {animal.get('kindCd', 'N/A')}")
        print(f"  - 성별: {animal.get('sexCd', 'N/A')}")
        print(f"  - 나이: {animal.get('age', 'N/A')}")
        print(f"  - 몸무게: {animal.get('weight', 'N/A')}")
        print(f"  - 색상: {animal.get('colorCd', 'N/A')}")
        print(f"  - 발견장소: {animal.get('happenPlace', 'N/A')}")
        print(f"  - 공고번호: {animal.get('noticeNo', 'N/A')}")
        print(f"  - 이미지 URL: {animal.get('popfile', 'N/A')[:50]}...")
        print(f"  - 특징: {animal.get('specialMark', 'N/A')[:50]}")
        print()
    
    print("=" * 50 + "\n")
    
    # 3. 이미지 URL 테스트
    print("3️⃣ 이미지 URL 접근 테스트")
    print("-" * 50)
    
    import requests
    success_count = 0
    fail_count = 0
    
    for i, animal in enumerate(animals[:3], 1):  # 처음 3개만 테스트
        image_url = animal.get('popfile', '')
        if image_url:
            try:
                response = requests.head(image_url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ 동물 #{i} 이미지 접근 가능")
                    success_count += 1
                else:
                    print(f"⚠️  동물 #{i} 이미지 상태 코드: {response.status_code}")
                    fail_count += 1
            except Exception as e:
                print(f"❌ 동물 #{i} 이미지 접근 실패: {str(e)[:50]}")
                fail_count += 1
        else:
            print(f"⚠️  동물 #{i} 이미지 URL 없음")
            fail_count += 1
    
    print(f"\n이미지 접근 결과: 성공 {success_count}개, 실패 {fail_count}개")
    print("\n" + "=" * 50 + "\n")
    
    print("🎉 모든 테스트가 완료되었습니다!")
    return True


if __name__ == "__main__":
    try:
        test_api_connection()
    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

