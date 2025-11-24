"""
완전 자동화 스크립트: 데이터 수집 → 이미지 생성 → 인스타그램 포스팅
"""
import os
import sys
from datetime import datetime
from fetch_animals import AnimalDataFetcher
from instagram_poster import InstagramPoster, main as instagram_main

def main():
    """완전 자동화 메인 함수"""
    print("🚀 유기동물 인스타그램 자동 포스팅 시작!")
    print("=" * 60)
    
    # 1단계: 동물 데이터 수집
    print("📡 1단계: 유기동물 데이터 수집 중...")
    
    api_key = os.getenv(
        'ANIMAL_API_KEY',
        'Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D'
    )
    
    fetcher = AnimalDataFetcher(api_key)
    animals = fetcher.get_recent_animals(count=5)
    
    if not animals:
        print("❌ 동물 데이터를 가져올 수 없습니다.")
        return False
    
    # 데이터 저장
    today = datetime.now().strftime('%Y-%m-%d')
    output_dir = os.path.join(
        os.path.dirname(__file__),
        'data',
        today
    )
    output_file = os.path.join(output_dir, 'animals.json')
    fetcher.save_to_json(animals, output_file)
    
    print(f"✅ {len(animals)}마리의 동물 데이터 수집 완료!")
    
    # 2단계: 인스타그램 자동 포스팅
    print("\n📤 2단계: 인스타그램 자동 포스팅 중...")
    
    success = instagram_main()
    
    if success:
        print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
        print("✅ 데이터 수집 완료")
        print("✅ 인스타그램 포스팅 완료")
        return True
    else:
        print("\n❌ 인스타그램 포스팅에 실패했습니다.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
