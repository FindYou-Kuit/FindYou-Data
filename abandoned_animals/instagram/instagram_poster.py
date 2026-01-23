"""
Instagram Business API를 사용한 포스팅 (image_url 방식)
외부 이미지 URL을 받아서 Instagram에 직접 포스팅
"""
import requests
import time
import os
from typing import Dict

class InstagramPoster:
    def __init__(self, page_access_token: str, instagram_business_id: str):
        """
        Instagram Business API 포스터
        
        Args:
            page_access_token: Facebook Page Access Token
            instagram_business_id: Instagram Business Account ID
        """
        self.page_access_token = page_access_token
        self.instagram_business_id = instagram_business_id
        self.graph_api_version = "v20.0"
        self.base_url = f"https://graph.facebook.com/{self.graph_api_version}"
        
    def validate_connection(self) -> Dict:
        """연결 상태 검증"""
        try:
            url = f"{self.base_url}/{self.instagram_business_id}"
            params = {
                'fields': 'id,username,name,media_count',
                'access_token': self.page_access_token
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                account_info = response.json()
                return {
                    'success': True,
                    'account_info': account_info,
                    'message': f"연결 성공: @{account_info.get('username', 'N/A')}"
                }
            else:
                return {
                    'success': False,
                    'error': response.json(),
                    'message': f"계정 접근 실패: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"연결 검증 중 오류: {e}"
            }
    
    def create_media_container(self, image_url: str, caption: str) -> Dict:
        """미디어 컨테이너 생성"""
        try:
            url = f"{self.base_url}/{self.instagram_business_id}/media"
            data = {
                'image_url': image_url,
                'caption': caption,
                'access_token': self.page_access_token
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                container_id = result.get('id')
                
                return {
                    'success': True,
                    'container_id': container_id,
                    'message': f"미디어 컨테이너 생성 성공: {container_id}"
                }
            else:
                error_data = response.json()
                return {
                    'success': False,
                    'error': error_data,
                    'message': f"컨테이너 생성 실패: {error_data.get('error', {}).get('message', 'Unknown error')}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"컨테이너 생성 중 오류: {e}"
            }
    
    def check_container_status(self, container_id: str, max_wait_time: int = 300) -> Dict:
        """컨테이너 상태 확인 및 대기"""
        try:
            url = f"{self.base_url}/{container_id}"
            params = {
                'fields': 'status_code',
                'access_token': self.page_access_token
            }
            
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status_code')
                    
                    print(f"컨테이너 상태: {status}")
                    
                    if status == 'FINISHED':
                        return {
                            'success': True,
                            'status': status,
                            'message': "컨테이너 준비 완료"
                        }
                    elif status in ['ERROR', 'EXPIRED']:
                        return {
                            'success': False,
                            'status': status,
                            'message': f"컨테이너 처리 실패: {status}"
                        }
                    elif status == 'IN_PROGRESS':
                        print("처리 중... 30초 대기")
                        time.sleep(30)
                        continue
                else:
                    return {
                        'success': False,
                        'error': response.json(),
                        'message': f"상태 확인 실패: {response.status_code}"
                    }
            
            return {
                'success': False,
                'message': f"시간 초과: {max_wait_time}초 내에 처리되지 않음"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"상태 확인 중 오류: {e}"
            }
    
    def publish_media(self, container_id: str) -> Dict:
        """미디어 게시"""
        try:
            url = f"{self.base_url}/{self.instagram_business_id}/media_publish"
            data = {
                'creation_id': container_id,
                'access_token': self.page_access_token
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                media_id = result.get('id')
                
                return {
                    'success': True,
                    'media_id': media_id,
                    'message': f"포스트 게시 성공! 미디어 ID: {media_id}"
                }
            else:
                error_data = response.json()
                return {
                    'success': False,
                    'error': error_data,
                    'message': f"게시 실패: {error_data.get('error', {}).get('message', 'Unknown error')}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"게시 중 오류: {e}"
            }
    
    def post_image(self, image_url: str, caption: str) -> Dict:
        """
        완전한 Instagram 포스팅 프로세스
        
        Args:
            image_url: 공개 이미지 URL (https://...)
            caption: 포스트 캡션
            
        Returns:
            포스팅 결과
        """
        print("🚀 Instagram 포스팅 시작...")
        
        # 1단계: 연결 검증
        print("1️⃣ 연결 상태 검증 중...")
        validation = self.validate_connection()
        if not validation['success']:
            return validation
        
        print(f"✅ {validation['message']}")
        
        # 2단계: 미디어 컨테이너 생성
        print("2️⃣ 미디어 컨테이너 생성 중...")
        container_result = self.create_media_container(image_url, caption)
        if not container_result['success']:
            return container_result
        
        container_id = container_result['container_id']
        print(f"✅ {container_result['message']}")
        
        # 3단계: 컨테이너 상태 확인
        print("3️⃣ 컨테이너 처리 상태 확인 중...")
        status_result = self.check_container_status(container_id)
        if not status_result['success']:
            return status_result
        
        print(f"✅ {status_result['message']}")
        
        # 4단계: 미디어 게시
        print("4️⃣ 미디어 게시 중...")
        publish_result = self.publish_media(container_id)
        if not publish_result['success']:
            return publish_result
        
        print(f"🎉 {publish_result['message']}")
        
        return {
            'success': True,
            'media_id': publish_result['media_id'],
            'container_id': container_id,
            'account_info': validation['account_info'],
            'message': "Instagram 포스트가 성공적으로 게시되었습니다!"
        }


def main():
    """메인 실행 함수 - 환경변수에서 토큰 정보 가져와서 테스트"""
    page_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
    
    if not page_token or not account_id:
        print("❌ 환경변수 INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID가 필요합니다.")
        return
    
    # 테스트용 이미지와 캡션
    test_image_url = "https://images.pexels.com/photos/1366942/pexels-photo-1366942.jpeg"
    test_caption = "테스트 포스트입니다.\n\n#테스트 #FindYou"
    
    # Instagram 포스터 초기화 및 포스팅
    poster = InstagramPoster(page_token, account_id)
    result = poster.post_image(test_image_url, test_caption)
    
    print("\n" + "="*60)
    print("📊 최종 결과")
    print("="*60)
    
    if result['success']:
        print("🎉 성공!")
        print(f"미디어 ID: {result['media_id']}")
        print(f"계정: @{result['account_info']['username']}")
    else:
        print("❌ 실패!")
        print(f"오류: {result['message']}")
        if 'error' in result:
            print(f"상세: {result['error']}")


if __name__ == "__main__":
    main()
