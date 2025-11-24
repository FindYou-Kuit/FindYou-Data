"""
XML 형식으로 API 테스트 - JSON이 아닌 XML로 시도
"""
import requests
from urllib.parse import unquote
import xml.etree.ElementTree as ET

api_key = "Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D"

print("=" * 70)
print("XML 형식으로 시도 조회 API 테스트")
print("=" * 70)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/sido"
params = {
    'serviceKey': unquote(api_key),
    'numOfRows': '17'
    # _type을 지정하지 않으면 기본이 XML
}

try:
    response = requests.get(url, params=params)
    print(f"상태 코드: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"\n응답 내용:\n{response.text[:1000]}\n")
    
    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            print("✅ XML 파싱 성공!")
            print(f"루트 태그: {root.tag}")
            
            # 헤더 확인
            header = root.find('.//header')
            if header is not None:
                result_code = header.find('resultCode')
                result_msg = header.find('resultMsg')
                print(f"\n📋 헤더:")
                print(f"  - 결과코드: {result_code.text if result_code is not None else 'N/A'}")
                print(f"  - 결과메시지: {result_msg.text if result_msg is not None else 'N/A'}")
            
            # 바디 확인
            body = root.find('.//body')
            if body is not None:
                items = body.findall('.//item')
                print(f"\n📊 바디:")
                print(f"  - 조회된 항목 수: {len(items)}")
                
                if items:
                    print(f"\n첫 번째 항목:")
                    for child in items[0]:
                        print(f"    {child.tag}: {child.text}")
        except ET.ParseError as e:
            print(f"❌ XML 파싱 실패: {e}")
except Exception as e:
    print(f"❌ 요청 실패: {e}")

print("\n" + "=" * 70)
print("XML 형식으로 유기동물 조회 API 테스트")
print("=" * 70)

from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

url = "http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic"
params = {
    'serviceKey': unquote(api_key),
    'bgnde': start_date.strftime('%Y%m%d'),
    'endde': end_date.strftime('%Y%m%d'),
    'pageNo': '1',
    'numOfRows': '5'
}

print(f"기간: {start_date.strftime('%Y%m%d')} ~ {end_date.strftime('%Y%m%d')}")

try:
    response = requests.get(url, params=params)
    print(f"상태 코드: {response.status_code}")
    print(f"\n응답 내용:\n{response.text[:2000]}\n")
    
    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            print("✅ XML 파싱 성공!")
            
            # 헤더 확인
            header = root.find('.//header')
            if header is not None:
                result_code = header.find('resultCode')
                result_msg = header.find('resultMsg')
                print(f"\n📋 헤더:")
                print(f"  - 결과코드: {result_code.text if result_code is not None else 'N/A'}")
                print(f"  - 결과메시지: {result_msg.text if result_msg is not None else 'N/A'}")
            
            # 바디 확인
            body = root.find('.//body')
            if body is not None:
                total_count = body.find('totalCount')
                print(f"\n📊 바디:")
                print(f"  - 총 개수: {total_count.text if total_count is not None else 'N/A'}")
                
                items = body.findall('.//item')
                print(f"  - 조회된 동물: {len(items)}마리")
                
                if items:
                    print(f"\n🐾 첫 번째 동물:")
                    for child in items[0]:
                        if child.tag in ['kindCd', 'noticeNo', 'happenPlace', 'popfile']:
                            print(f"    {child.tag}: {child.text}")
        except ET.ParseError as e:
            print(f"❌ XML 파싱 실패: {e}")
except Exception as e:
    print(f"❌ 요청 실패: {e}")
    import traceback
    traceback.print_exc()

