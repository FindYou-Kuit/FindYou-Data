"""
v2 API 직접 테스트 - 모든 가능한 방식 시도
"""
import requests
from datetime import datetime, timedelta
from urllib.parse import quote, unquote

# API 키 원본
api_key_encoded = "Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D"
api_key_decoded = unquote(api_key_encoded)

print("=" * 80)
print("테스트 1: 최소 파라미터로 v2 API 호출 (인코딩된 키)")
print("=" * 80)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic_v2"
params = {
    'serviceKey': api_key_encoded,
    '_type': 'json'
}

response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"URL: {response.url}")
print(f"응답:\n{response.text[:500]}\n")

print("=" * 80)
print("테스트 2: 최소 파라미터로 v2 API 호출 (디코딩된 키)")
print("=" * 80)

params = {
    'serviceKey': api_key_decoded,
    '_type': 'json'
}

response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답:\n{response.text[:500]}\n")

print("=" * 80)
print("테스트 3: 날짜 없이 페이지 정보만 (디코딩된 키)")
print("=" * 80)

params = {
    'serviceKey': api_key_decoded,
    'pageNo': '1',
    'numOfRows': '10',
    '_type': 'json'
}

response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답:\n{response.text[:500]}\n")

print("=" * 80)
print("테스트 4: 최근 30일 데이터 조회 (디코딩된 키)")
print("=" * 80)

end_date = datetime.now()
start_date = end_date - timedelta(days=30)

params = {
    'serviceKey': api_key_decoded,
    'bgnde': start_date.strftime('%Y%m%d'),
    'endde': end_date.strftime('%Y%m%d'),
    'pageNo': '1',
    'numOfRows': '10',
    '_type': 'json'
}

print(f"기간: {start_date.strftime('%Y%m%d')} ~ {end_date.strftime('%Y%m%d')}")
response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답:\n{response.text[:1000]}\n")

if response.status_code == 200:
    try:
        data = response.json()
        print("✅ JSON 파싱 성공!")
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
                
                if 'items' in body and body['items']:
                    items = body['items'].get('item', [])
                    if isinstance(items, list):
                        print(f"  조회된 동물: {len(items)}마리")
                        if items:
                            print(f"\n첫 번째 동물:")
                            print(f"  품종: {items[0].get('kindCd')}")
                            print(f"  공고번호: {items[0].get('noticeNo')}")
                            print(f"  발견장소: {items[0].get('happenPlace')}")
                    elif isinstance(items, dict):
                        print(f"  조회된 동물: 1마리")
                        print(f"\n동물:")
                        print(f"  품종: {items.get('kindCd')}")
                        print(f"  공고번호: {items.get('noticeNo')}")
    except Exception as e:
        print(f"파싱 오류: {e}")

print("\n" + "=" * 80)
print("테스트 5: XML 형식으로 시도 (디코딩된 키)")
print("=" * 80)

params = {
    'serviceKey': api_key_decoded,
    'pageNo': '1',
    'numOfRows': '5'
    # _type 없으면 기본 XML
}

response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"응답:\n{response.text[:1000]}\n")

print("=" * 80)
print("최종 결론")
print("=" * 80)

if response.status_code == 500:
    print("❌ API 키 문제 가능성:")
    print("1. 공공데이터포털에서 활용신청이 승인되지 않음")
    print("2. API 키가 잘못됨 (다른 서비스의 키)")
    print("3. API 서비스 장애")
    print("\n📝 해결 방법:")
    print("1. https://www.data.go.kr 로그인")
    print("2. 마이페이지 > 오픈API > 인증키 발급현황")
    print("3. '국가동물보호정보시스템 구조동물 조회 서비스' 확인")
    print("4. 상태가 '승인'인지 확인")
    print("5. '일반 인증키 (Encoding)' 복사")

