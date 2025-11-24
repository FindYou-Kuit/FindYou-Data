"""
올바른 URL로 테스트
"""
import requests
from urllib.parse import unquote

api_key = "Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D"
api_key_decoded = unquote(api_key)

print("=" * 80)
print("올바른 URL로 테스트!")
print("=" * 80)

# 올바른 URL
url = "https://apis.data.go.kr/1543061/abandonmentPublicService_v2/abandonmentPublic_v2"

print(f"URL: {url}")
print(f"API 키: {api_key_decoded[:20]}...{api_key_decoded[-10:]}")
print()

# 테스트 1: 최소 파라미터
print("테스트 1: 최소 파라미터")
params = {
    'serviceKey': api_key_decoded,
    '_type': 'json'
}

response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:500]}")

if response.status_code == 200:
    try:
        data = response.json()
        print("🎉 JSON 파싱 성공!")
        print(f"응답 키: {list(data.keys())}")
        
        if 'response' in data:
            resp = data['response']
            if 'header' in resp:
                header = resp['header']
                print(f"\n헤더:")
                print(f"  결과코드: {header.get('resultCode')}")
                print(f"  결과메시지: {header.get('resultMsg')}")
            
            if 'body' in resp:
                body = resp['body']
                print(f"\n바디:")
                print(f"  총 개수: {body.get('totalCount')}")
    except Exception as e:
        print(f"JSON 파싱 실패: {e}")

print("\n" + "=" * 80)
print("테스트 2: 페이지 파라미터 추가")
print("=" * 80)

params = {
    'serviceKey': api_key_decoded,
    'pageNo': '1',
    'numOfRows': '10',
    '_type': 'json'
}

response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:1000]}")

if response.status_code == 200:
    try:
        data = response.json()
        print("🎉 성공!")
        
        if 'response' in data and 'body' in data['response']:
            body = data['response']['body']
            total_count = body.get('totalCount', 0)
            print(f"총 동물 수: {total_count}")
            
            if 'items' in body and body['items']:
                items = body['items']
                if 'item' in items:
                    animals = items['item']
                    if isinstance(animals, list):
                        print(f"조회된 동물: {len(animals)}마리")
                        if animals:
                            print(f"\n첫 번째 동물:")
                            print(f"  품종: {animals[0].get('kindCd', 'N/A')}")
                            print(f"  공고번호: {animals[0].get('noticeNo', 'N/A')}")
                            print(f"  발견장소: {animals[0].get('happenPlace', 'N/A')}")
                    else:
                        print(f"조회된 동물: 1마리")
                        print(f"  품종: {animals.get('kindCd', 'N/A')}")
                        print(f"  공고번호: {animals.get('noticeNo', 'N/A')}")
                        
    except Exception as e:
        print(f"파싱 오류: {e}")
        import traceback
        traceback.print_exc()
