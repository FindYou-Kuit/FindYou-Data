"""
국가동물보호정보시스템 API를 사용하여 구조동물 데이터를 가져오는 스크립트
"""
import requests
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import unquote

class AnimalDataFetcher:
    def __init__(self, api_key: str):
        """
        Args:
            api_key: 공공데이터포털 API 인증키 (URL 인코딩된 형태)
        """
        # API 키가 인코딩되어 있다면 디코딩
        self.api_key = unquote(api_key)
        self.base_url = "https://apis.data.go.kr/1543061/abandonmentPublicService_v2"
        
    def fetch_abandoned_animals(
        self, 
        num_of_rows: int = 100,
        page_no: int = 1,
        upkind: Optional[str] = None,  # 417000: 개, 422400: 고양이, 429900: 기타
        state: str = "notice"  # notice: 공고중, protect: 보호중
    ) -> Dict:
        """
        유기동물 정보를 조회합니다.
        
        Args:
            num_of_rows: 한 페이지 결과 수 (최대 1000)
            page_no: 페이지 번호
            upkind: 축종 코드 (417000: 개, 422400: 고양이, 429900: 기타)
            state: 상태 (notice: 공고중, protect: 보호중, all: 전체)
        
        Returns:
            API 응답 데이터
        """
        endpoint = f"{self.base_url}/abandonmentPublic_v2"
        
        params = {
            'serviceKey': self.api_key,
            'numOfRows': str(num_of_rows),
            'pageNo': str(page_no),
            '_type': 'json'
        }
        
        if upkind:
            params['upkind'] = upkind
            
        if state != "all":
            params['state'] = state
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류 발생: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 중 오류 발생: {e}")
            return {}
    
    def get_recent_animals(self, count: int = 5) -> List[Dict]:
        """
        최신 공고 동물 정보를 가져옵니다.
        
        Args:
            count: 가져올 동물 수
        
        Returns:
            동물 정보 리스트
        """
        data = self.fetch_abandoned_animals(num_of_rows=count, page_no=1, state="notice")
        
        if not data or 'response' not in data:
            print("데이터를 가져올 수 없습니다.")
            return []
        
        response = data['response']
        
        # API 응답 구조 확인
        if 'body' not in response or 'items' not in response['body']:
            print("응답 데이터 구조가 올바르지 않습니다.")
            return []
        
        items = response['body']['items']
        
        # items가 딕셔너리인 경우 (item 키 확인)
        if isinstance(items, dict) and 'item' in items:
            animals = items['item']
        else:
            animals = items
        
        # 단일 항목인 경우 리스트로 변환
        if isinstance(animals, dict):
            animals = [animals]
        
        return animals[:count]
    
    def save_to_json(self, data: List[Dict], filepath: str):
        """
        데이터를 JSON 파일로 저장합니다.
        
        Args:
            data: 저장할 데이터
            filepath: 저장 경로
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"데이터가 {filepath}에 저장되었습니다.")


def main():
    # 환경변수에서 API 키 가져오기 (없으면 기본값 사용)
    api_key = os.getenv(
        'ANIMAL_API_KEY',
        'Mqn0b2BWoDH7qfXyzuOIfwA5O9dj4Dt9yOBuB4vGVpyMo5HOM0USlNPSzV5A5hfB%2FUhfl2yQHbIbMGs2luskgA%3D%3D'
    )
    
    fetcher = AnimalDataFetcher(api_key)
    
    # 최신 5마리 데이터 가져오기
    animals = fetcher.get_recent_animals(count=5)
    
    if not animals:
        print("가져온 동물 데이터가 없습니다.")
        return
    
    # 현재 날짜로 파일명 생성
    today = datetime.now().strftime('%Y-%m-%d')
    output_dir = os.path.join(
        os.path.dirname(__file__),
        'data',
        today
    )
    output_file = os.path.join(output_dir, 'animals.json')
    
    # 데이터 저장
    fetcher.save_to_json(animals, output_file)
    
    # 간단한 정보 출력
    print(f"\n총 {len(animals)}마리의 동물 정보를 가져왔습니다:")
    for i, animal in enumerate(animals, 1):
        print(f"{i}. {animal.get('kindCd', 'N/A')} - "
              f"발견장소: {animal.get('happenPlace', 'N/A')} - "
              f"공고번호: {animal.get('noticeNo', 'N/A')}")


if __name__ == "__main__":
    main()

