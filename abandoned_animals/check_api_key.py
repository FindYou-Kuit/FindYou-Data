"""
API 키 상태 확인 스크립트
공공데이터포털 API 키가 제대로 작동하는지 확인합니다.
"""
import os
import sys
from urllib.parse import unquote

def check_api_key():
    """API 키 상태를 확인합니다."""
    print("=" * 60)
    print("🔑 API 키 확인")
    print("=" * 60)
    print()
    
    # 환경변수에서 API 키 확인
    api_key = os.getenv('ANIMAL_API_KEY')
    
    if not api_key:
        print("⚠️  환경변수 ANIMAL_API_KEY가 설정되지 않았습니다.")
        print()
        print("📝 설정 방법:")
        print("  export ANIMAL_API_KEY='your_api_key_here'")
        print()
        
        # 기본값 사용
        api_key = 'Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D'
        print("ℹ️  코드에 하드코딩된 기본 API 키를 사용합니다.")
    else:
        print("✅ 환경변수에서 API 키를 찾았습니다.")
    
    print()
    print("-" * 60)
    print("API 키 정보:")
    print("-" * 60)
    
    # API 키 길이 확인
    print(f"길이: {len(api_key)} 문자")
    
    # URL 인코딩 상태 확인
    decoded_key = unquote(api_key)
    if api_key == decoded_key:
        print("상태: 디코딩됨 (일반 텍스트)")
    else:
        print("상태: 인코딩됨 (URL 인코딩)")
    
    # API 키 일부 표시 (보안상 일부만)
    if len(api_key) > 20:
        masked = api_key[:10] + "..." + api_key[-10:]
        print(f"값: {masked}")
    else:
        print(f"값: {api_key}")
    
    print()
    print("-" * 60)
    print("디코딩된 API 키:")
    print("-" * 60)
    if len(decoded_key) > 20:
        masked_decoded = decoded_key[:10] + "..." + decoded_key[-10:]
        print(f"값: {masked_decoded}")
    else:
        print(f"값: {decoded_key}")
    
    print()
    print("=" * 60)
    print("📋 다음 단계")
    print("=" * 60)
    print()
    print("1. test_api.py를 실행하여 API 연결을 테스트하세요:")
    print("   python test_api.py")
    print()
    print("2. API 키가 작동하지 않으면 다음을 확인하세요:")
    print("   - 공공데이터포털에서 활용신청이 승인되었는지 확인")
    print("   - '일반 인증키 (Encoding)'를 사용하고 있는지 확인")
    print("   - API 키를 최근에 재발급했는지 확인")
    print()
    print("3. 문제가 계속되면:")
    print("   - 공공데이터포털 고객센터: 1566-0025")
    print("   - 공공데이터포털: https://www.data.go.kr")
    print()


if __name__ == "__main__":
    check_api_key()

