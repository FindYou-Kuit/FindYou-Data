"""
파라미터를 하나씩 추가해가며 테스트
"""
import requests
from datetime import datetime, timedelta

api_key = "Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D"

print("=" * 80)
print("파라미터 조합 테스트")
print("=" * 80)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic_v2"

# 테스트 1: serviceKey만
print("테스트 1: serviceKey만")
params = {'serviceKey': api_key}
response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:100]}")
print()

# 테스트 2: serviceKey + _type
print("테스트 2: serviceKey + _type")
params = {
    'serviceKey': api_key,
    '_type': 'json'
}
response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:100]}")
print()

# 테스트 3: serviceKey + 날짜 (필수인지 확인)
print("테스트 3: serviceKey + 날짜")
today = datetime.now().strftime('%Y%m%d')
params = {
    'serviceKey': api_key,
    'bgnde': today,
    'endde': today
}
response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:100]}")
print()

# 테스트 4: serviceKey + 날짜 + _type
print("테스트 4: serviceKey + 날짜 + _type")
params = {
    'serviceKey': api_key,
    'bgnde': today,
    'endde': today,
    '_type': 'json'
}
response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:200]}")
print()

# 테스트 5: 모든 기본 파라미터
print("테스트 5: 모든 기본 파라미터")
params = {
    'serviceKey': api_key,
    'bgnde': today,
    'endde': today,
    'pageNo': '1',
    'numOfRows': '10',
    '_type': 'json'
}
response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:500]}")

if response.status_code == 200:
    try:
        data = response.json()
        print("✅ 성공!")
        print(f"응답 키: {list(data.keys())}")
    except:
        print("JSON 파싱 실패")
print()

# 테스트 6: XML로 시도
print("테스트 6: XML 형식")
params = {
    'serviceKey': api_key,
    'bgnde': today,
    'endde': today,
    'pageNo': '1',
    'numOfRows': '10'
}
response = requests.get(url, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:500]}")
