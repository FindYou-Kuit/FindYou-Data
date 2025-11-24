"""
가장 간단한 형태로 API 테스트
"""
import requests
import os

# GitHub Actions에서 사용하는 것과 동일한 방식
api_key = os.getenv('ANIMAL_API_KEY', 'Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D')

print("=" * 60)
print("🔑 API 키 상태")
print("=" * 60)
print(f"키 길이: {len(api_key)}")
print(f"키 시작: {api_key[:20]}...")
print(f"키 끝: ...{api_key[-20:]}")
print()

# 1. 가장 간단한 요청 (시도 조회)
print("=" * 60)
print("📍 테스트 1: 시도 조회 API")
print("=" * 60)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/sido"
params = {
    'serviceKey': api_key,
    '_type': 'json'
}

try:
    print(f"요청 URL: {url}")
    print(f"파라미터: {params}")
    print()
    
    response = requests.get(url, params=params, timeout=30)
    print(f"응답 코드: {response.status_code}")
    print(f"응답 헤더: {dict(response.headers)}")
    print(f"응답 내용: {response.text}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("✅ JSON 파싱 성공!")
            print(f"응답 구조: {list(data.keys())}")
        except:
            print("❌ JSON 파싱 실패")
    
except Exception as e:
    print(f"❌ 요청 실패: {e}")

print("\n" + "=" * 60)
print("🐾 테스트 2: 유기동물 조회 API (최소 파라미터)")
print("=" * 60)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic_v2"
params = {
    'serviceKey': api_key,
    '_type': 'json'
}

try:
    print(f"요청 URL: {url}")
    print(f"파라미터: {params}")
    print()
    
    response = requests.get(url, params=params, timeout=30)
    print(f"응답 코드: {response.status_code}")
    print(f"응답 내용: {response.text}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("✅ JSON 파싱 성공!")
            print(f"응답 구조: {list(data.keys())}")
        except:
            print("❌ JSON 파싱 실패")
    
except Exception as e:
    print(f"❌ 요청 실패: {e}")

print("\n" + "=" * 60)
print("🔍 결론")
print("=" * 60)

if response.status_code == 500:
    print("❌ 500 에러 - 다음 중 하나의 문제:")
    print("1. API 키가 승인되지 않음")
    print("2. API 키가 잘못됨")
    print("3. API 서비스 장애")
    print("4. 요청 파라미터 문제")
    print()
    print("📝 해결 방법:")
    print("1. 공공데이터포털 로그인")
    print("2. 마이페이지 > 오픈API > 인증키 발급현황")
    print("3. 해당 서비스 상태 확인")
    print("4. 필요시 재신청")
elif response.status_code == 200:
    print("✅ API 정상 작동!")
else:
    print(f"⚠️ 예상치 못한 응답 코드: {response.status_code}")
