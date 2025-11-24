"""
다양한 엔드포인트 URL 테스트
"""
import requests

api_key = "Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D"

# 가능한 엔드포인트들
endpoints = [
    # 기존 시도
    "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic_v2",
    
    # v1 버전
    "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic",
    
    # HTTPS 시도
    "https://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic_v2",
    "https://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic",
    
    # 다른 가능한 경로
    "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic2",
    "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublicV2",
    
    # 시도 조회 API (이건 작동해야 함)
    "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/sido",
    "https://apis.data.go.kr/1543061/abandonmentPublicSrvc/sido",
]

for i, url in enumerate(endpoints, 1):
    print(f"=" * 80)
    print(f"테스트 {i}: {url}")
    print("=" * 80)
    
    params = {
        'serviceKey': api_key,
        '_type': 'json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"상태 코드: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"응답 길이: {len(response.text)}")
        print(f"응답 내용: {response.text[:200]}")
        
        if response.status_code == 200:
            print("🎉 성공!")
            try:
                data = response.json()
                print(f"JSON 키: {list(data.keys())}")
                
                # 시도 조회라면 결과 확인
                if 'sido' in url:
                    items = data.get('response', {}).get('body', {}).get('items', {})
                    if 'item' in items:
                        print(f"시도 개수: {len(items['item']) if isinstance(items['item'], list) else 1}")
                        
            except Exception as e:
                print(f"JSON 파싱 실패: {e}")
        elif response.status_code != 500:
            print(f"⚠️ 500이 아닌 다른 에러: {response.status_code}")
        
    except Exception as e:
        print(f"❌ 요청 실패: {e}")
    
    print()
