"""
인스타그램 자동 포스팅 모듈
"""
import os
import json
from datetime import datetime
from io import BytesIO
import requests
from create_instagram_post import InstagramPostCreator

class InstagramPoster:
    def __init__(self, access_token: str, instagram_account_id: str):
        """
        Instagram Graph API를 사용한 자동 포스팅
        
        Args:
            access_token: Instagram Graph API 액세스 토큰
            instagram_account_id: 인스타그램 비즈니스 계정 ID
        """
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def upload_image_to_instagram(self, image_data: bytes, caption: str) -> bool:
        """
        이미지를 인스타그램에 직접 업로드
        
        Args:
            image_data: 이미지 바이너리 데이터
            caption: 포스트 캡션
            
        Returns:
            성공 여부
        """
        try:
            # 1단계: 이미지를 Facebook 서버에 업로드
            media_url = f"{self.base_url}/{self.instagram_account_id}/media"
            
            # 임시 파일로 이미지 저장 (Facebook API 요구사항)
            temp_file_path = "/tmp/temp_instagram_post.png"
            with open(temp_file_path, 'wb') as f:
                f.write(image_data)
            
            # 미디어 업로드
            files = {'image': open(temp_file_path, 'rb')}
            data = {
                'caption': caption,
                'access_token': self.access_token
            }
            
            response = requests.post(media_url, files=files, data=data)
            files['image'].close()
            
            # 임시 파일 삭제
            os.remove(temp_file_path)
            
            if response.status_code != 200:
                print(f"❌ 미디어 업로드 실패: {response.text}")
                return False
            
            media_id = response.json().get('id')
            print(f"✅ 미디어 업로드 성공: {media_id}")
            
            # 2단계: 미디어를 실제로 게시
            publish_url = f"{self.base_url}/{self.instagram_account_id}/media_publish"
            publish_data = {
                'creation_id': media_id,
                'access_token': self.access_token
            }
            
            publish_response = requests.post(publish_url, data=publish_data)
            
            if publish_response.status_code != 200:
                print(f"❌ 포스트 게시 실패: {publish_response.text}")
                return False
            
            post_id = publish_response.json().get('id')
            print(f"🎉 인스타그램 포스트 성공! ID: {post_id}")
            return True
            
        except Exception as e:
            print(f"❌ 인스타그램 업로드 중 오류: {e}")
            return False
    
    def create_caption(self, animals: list) -> str:
        """
        동물 정보를 바탕으로 캡션 생성
        
        Args:
            animals: 동물 정보 리스트
            
        Returns:
            인스타그램 캡션
        """
        today = datetime.now().strftime('%Y년 %m월 %d일')
        
        caption = f"""🐾 새로운 가족을 기다립니다 ({today})

오늘도 {len(animals)}마리의 소중한 친구들이 여러분을 기다리고 있어요.
따뜻한 가정에서 사랑받을 권리가 있습니다.

📋 오늘의 친구들:
"""
        
        for i, animal in enumerate(animals, 1):
            kind = animal.get('kindFullNm', animal.get('kindCd', 'N/A'))
            notice_no = animal.get('noticeNo', 'N/A')
            place = animal.get('happenPlace', 'N/A')
            
            # 품종명에서 대괄호 제거
            if '[' in kind and ']' in kind:
                kind = kind.split(']')[1].strip() if ']' in kind else kind
            
            # 발견장소 간략화
            if len(place) > 20:
                place = place[:20] + "..."
            
            caption += f"{i}. {kind} (공고번호: {notice_no})\n"
        
        caption += f"""
❤️ 입양 문의는 각 공고번호로 해당 보호센터에 연락하세요.

🏠 이 아이들에게는 여러분의 사랑이 필요합니다.
💕 입양은 또 다른 생명을 구하는 일입니다.

#유기동물 #입양 #반려동물 #유기견 #유기묘 
#동물보호 #입양문의 #사지말고입양하세요 
#반려동물입양 #유기동물보호 #새가족찾기
#FindYou #동물사랑 #생명존중"""

        return caption


def main():
    """메인 실행 함수"""
    print("🤖 인스타그램 자동 포스팅 시작...")
    
    # 환경변수에서 인스타그램 정보 가져오기
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
    
    if not access_token or not account_id:
        print("❌ 인스타그램 환경변수가 설정되지 않았습니다.")
        print("INSTAGRAM_ACCESS_TOKEN과 INSTAGRAM_ACCOUNT_ID를 설정하세요.")
        return False
    
    # 오늘 날짜의 동물 데이터 로드
    today = datetime.now().strftime('%Y-%m-%d')
    data_file = os.path.join(
        os.path.dirname(__file__),
        'data',
        today,
        'animals.json'
    )
    
    if not os.path.exists(data_file):
        print(f"❌ 동물 데이터 파일을 찾을 수 없습니다: {data_file}")
        print("먼저 fetch_animals.py를 실행하여 데이터를 수집하세요.")
        return False
    
    # 동물 데이터 로드
    with open(data_file, 'r', encoding='utf-8') as f:
        animals = json.load(f)
    
    if not animals:
        print("❌ 동물 데이터가 비어있습니다.")
        return False
    
    print(f"📊 {len(animals)}마리의 동물 데이터를 로드했습니다.")
    
    # 이미지 생성 (메모리에서)
    print("🎨 인스타그램 이미지 생성 중...")
    creator = InstagramPostCreator()
    image = creator.create_simple_grid(animals)
    
    # 이미지를 바이트로 변환
    img_buffer = BytesIO()
    image.save(img_buffer, format='PNG', quality=95)
    image_data = img_buffer.getvalue()
    
    print(f"✅ 이미지 생성 완료 ({len(image_data)} bytes)")
    
    # 캡션 생성
    poster = InstagramPoster(access_token, account_id)
    caption = poster.create_caption(animals)
    
    print("📝 캡션 생성 완료:")
    print("-" * 50)
    print(caption[:200] + "..." if len(caption) > 200 else caption)
    print("-" * 50)
    
    # 인스타그램에 업로드
    print("📤 인스타그램에 업로드 중...")
    success = poster.upload_image_to_instagram(image_data, caption)
    
    if success:
        print("🎉 인스타그램 자동 포스팅 완료!")
        return True
    else:
        print("❌ 인스타그램 포스팅 실패")
        return False


if __name__ == "__main__":
    main()
