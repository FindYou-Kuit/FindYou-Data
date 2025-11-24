"""
다양한 방식으로 API 테스트
"""
import requests
from urllib.parse import quote, unquote
from datetime import datetime, timedelta

api_key = "Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D"

print("=" * 70)
print("테스트 1: 시도 조회 API (가장 간단한 API)")
print("=" * 70)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/sido"
params = {
    'serviceKey': api_key,
    'numOfRows': '17',
    '_type': 'json'
}

try:
    response = requests.get(url, params=params)
    print(f"상태 코드: {response.status_code}")
    print(f"응답 길이: {len(response.text)}")
    print(f"응답 내용:\n{response.text[:500]}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ JSON 파싱 성공!")
        if 'response' in data:
            items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            print(f"✅ 시도 개수: {len(items) if isinstance(items, list) else 1}")
            if items:
                print(f"첫 번째 시도: {items[0] if isinstance(items, list) else items}")
except Exception as e:
    print(f"❌ 오류: {e}")

print("\n" + "=" * 70)
print("테스트 2: 품종 조회 API")
print("=" * 70)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/kind"
params = {
    'serviceKey': api_key,
    'up_kind_cd': '417000',  # 개
    '_type': 'json'
}

try:
    response = requests.get(url, params=params)
    print(f"상태 코드: {response.status_code}")
    print(f"응답 내용:\n{response.text[:500]}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ JSON 파싱 성공!")
        if 'response' in data:
            items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            print(f"✅ 품종 개수: {len(items) if isinstance(items, list) else 1}")
except Exception as e:
    print(f"❌ 오류: {e}")

print("\n" + "=" * 70)
print("테스트 3: 유기동물 조회 (최근 7일)")
print("=" * 70)

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic"
params = {
    'serviceKey': api_key,
    'bgnde': start_date.strftime('%Y%m%d'),
    'endde': end_date.strftime('%Y%m%d'),
    'pageNo': '1',
    'numOfRows': '5',
    '_type': 'json'
}

print(f"기간: {start_date.strftime('%Y%m%d')} ~ {end_date.strftime('%Y%m%d')}")

try:
    response = requests.get(url, params=params)
    print(f"상태 코드: {response.status_code}")
    print(f"응답 내용:\n{response.text[:1000]}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ JSON 파싱 성공!")
        print(f"응답 구조: {list(data.keys())}")
        
        if 'response' in data:
            response_data = data['response']
            print(f"Response 키: {list(response_data.keys())}")
            
            if 'header' in response_data:
                header = response_data['header']
                print(f"\n📋 헤더:")
                print(f"  - 결과코드: {header.get('resultCode')}")
                print(f"  - 결과메시지: {header.get('resultMsg')}")
            
            if 'body' in response_data:
                body = response_data['body']
                print(f"\n📊 바디:")
                print(f"  - 총 개수: {body.get('totalCount')}")
                
                if 'items' in body:
                    items = body['items']
                    if isinstance(items, dict) and 'item' in items:
                        animals = items['item']
                        if isinstance(animals, list):
                            print(f"  - 조회된 동물: {len(animals)}마리")
                            if animals:
                                print(f"\n🐾 첫 번째 동물:")
                                print(f"  - 품종: {animals[0].get('kindCd', 'N/A')}")
                                print(f"  - 공고번호: {animals[0].get('noticeNo', 'N/A')}")
                        else:
                            print(f"  - 조회된 동물: 1마리")
                            print(f"\n🐾 동물 정보:")
                            print(f"  - 품종: {animals.get('kindCd', 'N/A')}")
                            print(f"  - 공고번호: {animals.get('noticeNo', 'N/A')}")
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("테스트 4: 유기동물 조회 (오늘)")
print("=" * 70)

today = datetime.now().strftime('%Y%m%d')

params = {
    'serviceKey': api_key,
    'bgnde': today,
    'endde': today,
    'pageNo': '1',
    'numOfRows': '10',
    '_type': 'json'
}

print(f"날짜: {today}")

try:
    response = requests.get(url, params=params)
    print(f"상태 코드: {response.status_code}")
    print(f"응답 내용:\n{response.text[:500]}\n")
    
    if response.status_code == 200:
        data = response.json()
        body = data.get('response', {}).get('body', {})
        print(f"✅ 오늘의 공고: {body.get('totalCount', 0)}건")
except Exception as e:
    print(f"❌ 오류: {e}")

print("\n" + "=" * 70)
print("결론")
print("=" * 70)
print("API 키가 유효하지 않거나 서비스에 문제가 있는 것 같습니다.")
print("다음을 확인해주세요:")
print("1. 공공데이터포털에서 활용신청 승인 여부")
print("2. API 키 만료 여부")
print("3. 공공데이터포털 공지사항 확인")
print("\n📞 공공데이터포털 고객센터: 1566-0025")

