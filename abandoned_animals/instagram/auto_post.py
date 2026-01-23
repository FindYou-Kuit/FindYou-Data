"""
자동 Instagram 포스팅 메인 스크립트
외부에서 제공받은 이미지 URL과 캡션으로 Instagram에 포스팅
"""
import os
import sys
from instagram_poster import InstagramPoster

def post_to_instagram(image_url: str, caption: str) -> bool:
    """
    Instagram에 포스팅
    
    Args:
        image_url: 공개 이미지 URL (https://...)
        caption: 포스트 캡션
        
    Returns:
        성공 여부
    """
    # 환경변수에서 토큰 정보 가져오기
    page_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
    
    if not page_token or not account_id:
        print("❌ 환경변수 INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID가 필요합니다.")
        return False
    
    # Instagram 포스터 초기화 및 포스팅
    poster = InstagramPoster(page_token, account_id)
    result = poster.post_image(image_url, caption)
    
    if result['success']:
        print(f"🎉 Instagram 포스팅 성공!")
        print(f"계정: @{result['account_info']['username']}")
        print(f"미디어 ID: {result['media_id']}")
        return True
    else:
        print(f"❌ Instagram 포스팅 실패: {result['message']}")
        if 'error' in result:
            print(f"상세 오류: {result['error']}")
        return False


def main():
    """
    메인 실행 함수
    
    사용법:
    1. 환경변수 방식: python auto_post.py
    2. 인자 방식: python auto_post.py "이미지URL" "캡션"
    """
    if len(sys.argv) == 3:
        # 명령행 인자로 이미지 URL과 캡션 받기
        image_url = sys.argv[1]
        caption = sys.argv[2]
    else:
        # 기본 테스트용 (나중에 실제 구조동물 URL로 교체 예정)
        image_url = "https://images.pexels.com/photos/1366942/pexels-photo-1366942.jpeg"
        caption = """🐕 오늘의 친구를 소개합니다!

새로운 가족을 기다리고 있어요 💕

#유기동물 #입양 #FindYou #반려동물"""
    
    print(f"📸 이미지 URL: {image_url}")
    print(f"📝 캡션: {caption[:50]}...")
    print("-" * 60)
    
    success = post_to_instagram(image_url, caption)
    
    if success:
        print("\n✅ 자동 포스팅이 완료되었습니다!")
        sys.exit(0)
    else:
        print("\n❌ 자동 포스팅에 실패했습니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()