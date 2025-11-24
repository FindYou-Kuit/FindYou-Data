"""
API 키 형식 테스트 - 인코딩/디코딩 다양하게 시도
"""
import requests
from urllib.parse import quote, unquote

# 원본 키
api_key_original = "Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D"

# 다양한 형태로 변환
api_key_decoded = unquote(api_key_original)
api_key_double_decoded = unquote(api_key_decoded)
api_key_encoded = quote(api_key_decoded)

print("=" * 80)
print("API 키 형태 비교")
print("=" * 80)
print(f"원본:           {api_key_original}")
print(f"1차 디코딩:     {api_key_decoded}")
print(f"2차 디코딩:     {api_key_double_decoded}")
print(f"재인코딩:       {api_key_encoded}")
print()

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/sido"

keys_to_test = [
    ("원본 키", api_key_original),
    ("1차 디코딩", api_key_decoded),
    ("2차 디코딩", api_key_double_decoded),
    ("재인코딩", api_key_encoded),
]

for name, key in keys_to_test:
    print(f"=" * 80)
    print(f"테스트: {name}")
    print(f"키: {key}")
    print("=" * 80)
    
    params = {
        'serviceKey': key,
        '_type': 'json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.text[:100]}")
        
        if response.status_code == 200:
            print("🎉 성공!")
            try:
                data = response.json()
                print(f"JSON 파싱 성공! 키: {list(data.keys())}")
            except:
                print("JSON 파싱 실패")
        elif response.status_code == 401:
            print("❌ 401 - 인증 실패")
        elif response.status_code == 403:
            print("❌ 403 - 권한 없음")
        elif response.status_code != 500:
            print(f"⚠️ 다른 에러: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 요청 실패: {e}")
    
    print()

# 마지막으로 완전히 다른 방식 시도
print("=" * 80)
print("직접 URL 구성 테스트")
print("=" * 80)

# URL을 직접 구성해보기
base_url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/sido"
direct_url = f"{base_url}?serviceKey={api_key_decoded}&_type=json"

print(f"직접 구성한 URL: {direct_url}")

try:
    response = requests.get(direct_url, timeout=10)
    print(f"상태 코드: {response.status_code}")
    print(f"응답: {response.text[:200]}")
except Exception as e:
    print(f"❌ 요청 실패: {e}")
