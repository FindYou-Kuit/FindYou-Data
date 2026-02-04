"""
Instagram 자동 포스팅 전체 시퀀스
1. API에서 동물 데이터 가져오기 (지정 날짜)
2. 이미지 생성 (지정 날짜)
3. 이미지 URL 업로드 (FindYou CDN)
4. Instagram 캐러셀 포스팅 (지정 날짜)
"""
import os
import json
import time
import random
import requests
from dotenv import load_dotenv
from datetime import datetime
from create_image import ImageGenerator
from fetch_animals import AnimalDataFetcher

load_dotenv()


class InstagramAutoPost:
    def __init__(self):
        # FindYou CDN 설정
        self.cdn_url = os.getenv("FINDYOU_CDN_URL")
        self.cdn_token = os.getenv("FINDYOU_CDN_TOKEN")

        # Instagram 설정
        self.ig_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.ig_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        self.graph_api = "https://graph.facebook.com/v20.0"

        # 이미지 생성기
        self.image_generator = ImageGenerator()

        # API 키
        self.api_key = os.getenv('ANIMAL_API_KEY')
        
    def fetch_animals(self, target_date, count=7):
        """1. 동물 데이터 가져오기 (서울 1 + 경기 1 + 랜덤 5 = 총 7마리)"""
        print("=" * 60)
        print(f"1️⃣ 동물 데이터 가져오기 ({target_date.strftime('%Y-%m-%d')})")
        print("=" * 60)
        
        fetcher = AnimalDataFetcher(self.api_key)
        date_str = target_date.strftime('%Y%m%d')
        
        def parse_animals(data):
            """API 응답에서 동물 리스트 추출 및 이미지 필터링"""
            if not data or 'response' not in data:
                return []
            response = data['response']
            if 'body' not in response or 'items' not in response['body']:
                return []
            items = response['body']['items']
            if isinstance(items, dict) and 'item' in items:
                animals = items['item']
            else:
                animals = items
            if isinstance(animals, dict):
                animals = [animals]
            # 이미지 필터링
            result = []
            for animal in animals:
                popfile1 = animal.get('popfile1', '')
                if popfile1 and popfile1.startswith('http') and '/shelter/' in popfile1 and len(popfile1) > 80:
                    result.append(animal)
            return result
        
        selected = []
        selected_ids = set()  # desertionNo로 중복 체크
        
        # 1. 서울(6110000)에서 1마리
        print("\n📍 서울 데이터 조회 중...")
        seoul_data = fetcher.fetch_abandoned_animals(num_of_rows=100, bgnde=date_str, endde=date_str, upr_cd="6110000")
        seoul_animals = parse_animals(seoul_data)
        print(f"   - 서울: {len(seoul_animals)}마리 (이미지 있는 것)")
        
        if seoul_animals:
            seoul_pick = random.choice(seoul_animals)
            selected.append(seoul_pick)
            selected_ids.add(seoul_pick.get('desertionNo'))
            print(f"   ✅ 서울 1마리 선택: {seoul_pick.get('kindNm')} - {seoul_pick.get('careNm')}")
        
        # 2. 경기도(6410000)에서 1마리
        print("\n📍 경기도 데이터 조회 중...")
        gyeonggi_data = fetcher.fetch_abandoned_animals(num_of_rows=100, bgnde=date_str, endde=date_str, upr_cd="6410000")
        gyeonggi_animals = parse_animals(gyeonggi_data)
        print(f"   - 경기: {len(gyeonggi_animals)}마리 (이미지 있는 것)")
        
        if gyeonggi_animals:
            # 이미 선택된 것 제외
            available = [a for a in gyeonggi_animals if a.get('desertionNo') not in selected_ids]
            if available:
                gyeonggi_pick = random.choice(available)
                selected.append(gyeonggi_pick)
                selected_ids.add(gyeonggi_pick.get('desertionNo'))
                print(f"   ✅ 경기 1마리 선택: {gyeonggi_pick.get('kindNm')} - {gyeonggi_pick.get('careNm')}")
        
        # 3. 전체에서 나머지 선택 (5마리)
        remaining_count = count - len(selected)
        if remaining_count > 0:
            print(f"\n📍 전체 데이터 조회 중 (랜덤 {remaining_count}마리)...")
            all_data = fetcher.fetch_abandoned_animals(num_of_rows=100, bgnde=date_str, endde=date_str)
            all_animals = parse_animals(all_data)
            print(f"   - 전체: {len(all_animals)}마리 (이미지 있는 것)")
            
            # 이미 선택된 것 제외
            available = [a for a in all_animals if a.get('desertionNo') not in selected_ids]
            
            if len(available) >= remaining_count:
                random_picks = random.sample(available, remaining_count)
            else:
                random_picks = available
            
            for pick in random_picks:
                selected.append(pick)
                selected_ids.add(pick.get('desertionNo'))
            
            print(f"   ✅ 랜덤 {len(random_picks)}마리 선택")
        
        animals = selected
        
        print(f"✅ {len(animals)}마리 데이터 가져오기 완료")
        for i, animal in enumerate(animals):
            print(f"   {i+1}. {animal.get('kindNm', 'N/A')} - {animal.get('careNm', 'N/A')}")
        
        return animals
    
    def generate_images(self, animals, target_date):
        """2. 이미지 생성 (지정 날짜)"""
        print("\n" + "=" * 60)
        print(f"2️⃣ 이미지 생성 ({target_date.strftime('%Y-%m-%d')})")
        print("=" * 60)
        
        image_paths = []
        
        for i, animal in enumerate(animals):
            print(f"\n[{i+1}/{len(animals)}] {animal.get('kindNm', 'N/A')} 이미지 생성 중...")
            result = self.image_generator.create_image(animal, target_date=target_date)
            
            if result['success']:
                image_paths.append(result['path'])
                print(f"   ✅ {result['path']}")
            else:
                print(f"   ❌ 실패: {result.get('error')}")
        
        print(f"\n✅ 총 {len(image_paths)}개 이미지 생성 완료")
        return image_paths
    
    def upload_to_cdn(self, image_paths):
        """3. CDN에 이미지 업로드"""
        print("\n" + "=" * 60)
        print("3️⃣ CDN 업로드")
        print("=" * 60)
        
        if not self.cdn_token:
            raise Exception("FINDYOU_CDN_TOKEN 환경변수가 필요합니다.")
        
        urls = []
        headers = {"Authorization": f"Bearer {self.cdn_token}"}
        
        for i, path in enumerate(image_paths):
            print(f"\n[{i+1}/{len(image_paths)}] 업로드 중: {os.path.basename(path)}")
            
            with open(path, 'rb') as f:
                files = {'files': (os.path.basename(path), f, 'image/jpeg')}
                response = requests.post(self.cdn_url, headers=headers, files=files)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data', {}).get('urls'):
                    url = data['data']['urls'][0]
                    urls.append(url)
                    print(f"   ✅ {url}")
                else:
                    print(f"   ❌ 업로드 실패: {data}")
            else:
                print(f"   ❌ HTTP 오류: {response.status_code}")
        
        print(f"\n✅ 총 {len(urls)}개 URL 생성 완료")
        return urls
    
    def generate_hashtags(self, animals):
        """동물 데이터 기반 해시태그 생성"""
        tags = set()
        
        for animal in animals:
            # 지역
            org_nm = animal.get('orgNm', '')
            if '충청북' in org_nm or '충북' in org_nm:
                tags.add('#충북')
            if '보은' in org_nm:
                tags.add('#보은')
            if '부산' in org_nm:
                tags.add('#부산')
            if '남구' in org_nm:
                tags.add('#남구')
            if '세종' in org_nm:
                tags.add('#세종')
            if '전북' in org_nm or '전라북' in org_nm:
                tags.add('#전북')
            if '전주' in org_nm:
                tags.add('#전주')
            if '경북' in org_nm or '경상북' in org_nm:
                tags.add('#경북')
            if '대구' in org_nm:
                tags.add('#대구')
            if '경기' in org_nm:
                tags.add('#경기')
            if '서울' in org_nm:
                tags.add('#서울')
            if '인천' in org_nm:
                tags.add('#인천')
            if '제주' in org_nm:
                tags.add('#제주')
            
            # 동물 종류
            up_kind = animal.get('upKindNm', '')
            if up_kind == '개':
                tags.add('#강아지')
                tags.add('#유기견')
            elif up_kind == '고양이':
                tags.add('#고양이')
                tags.add('#유기묘')
            
            # 품종 (띄어쓰기 제거, 2글자 이상만)
            kind_nm = animal.get('kindNm', '').replace(' ', '')
            if kind_nm and len(kind_nm) >= 2 and kind_nm not in ['기타']:
                tags.add(f'#{kind_nm}')
            
            # 색상 (2글자 이상만)
            color = animal.get('colorCd', '')
            clean_colors = ['흰색', '검정', '갈색', '황색', '회색', '황갈색', '크림', '흑색', '백색']
            for c in clean_colors:
                if c in color:
                    tags.add(f'#{c}')
            
            # 보호센터 (띄어쓰기 제거)
            care_nm = animal.get('careNm', '').replace(' ', '')
            if care_nm and len(care_nm) >= 2:
                tags.add(f'#{care_nm}')
        
        # 고정 태그
        fixed_tags = ['#찾아유', '#유기동물', '#입양', '#사지말고입양하세요']
        for tag in fixed_tags:
            tags.add(tag)
        
        return ' '.join(sorted(tags))
    
    def generate_caption(self, animals, target_date):
        """캡션 생성 (지정 날짜)"""
        date_str = target_date.strftime('%Y년 %m월 %d일')
        hashtags = self.generate_hashtags(animals)
        
        caption = f"""🐾 {date_str} 보호동물 공고

새로운 가족을 기다리는 아이들이에요 💕
👉 스와이프해서 모두 확인해주세요!

📋 더 많은 보호동물 보기
👉 https://www.animal.go.kr/front/awtis/public/publicList.do

{hashtags}"""
        
        return caption
    
    def post_to_instagram(self, urls, animals, target_date):
        """4. Instagram 캐러셀 포스팅"""
        print("\n" + "=" * 60)
        print("4️⃣ Instagram 포스팅")
        print("=" * 60)
        
        if not self.ig_token:
            raise Exception("INSTAGRAM_ACCESS_TOKEN 환경변수가 필요합니다.")
        
        caption = self.generate_caption(animals, target_date)
        print(f"\n📝 캡션:\n{caption}\n")
        
        # 캐러셀 아이템 생성
        print("캐러셀 아이템 생성 중...")
        item_ids = []
        
        for i, url in enumerate(urls):
            print(f"   [{i+1}/{len(urls)}] 아이템 생성...")
            response = requests.post(
                f"{self.graph_api}/{self.ig_account_id}/media",
                data={
                    "image_url": url,
                    "is_carousel_item": "true",
                    "access_token": self.ig_token
                }
            )
            
            if response.status_code == 200:
                item_id = response.json().get('id')
                item_ids.append(item_id)
                print(f"      ✅ ID: {item_id}")
            else:
                print(f"      ❌ 실패: {response.json()}")
        
        if len(item_ids) < 2:
            raise Exception("캐러셀에는 최소 2개 이미지가 필요합니다.")
        
        # 캐러셀 컨테이너 생성
        print("\n캐러셀 컨테이너 생성 중...")
        response = requests.post(
            f"{self.graph_api}/{self.ig_account_id}/media",
            data={
                "media_type": "CAROUSEL",
                "children": ",".join(item_ids),
                "caption": caption,
                "access_token": self.ig_token
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"캐러셀 생성 실패: {response.json()}")
        
        carousel_id = response.json().get('id')
        print(f"   ✅ 캐러셀 ID: {carousel_id}")
        
        # 잠시 대기
        print("\n처리 대기 중...")
        time.sleep(3)
        
        # 게시
        print("게시 중...")
        response = requests.post(
            f"{self.graph_api}/{self.ig_account_id}/media_publish",
            data={
                "creation_id": carousel_id,
                "access_token": self.ig_token
            }
        )
        
        if response.status_code == 200:
            media_id = response.json().get('id')
            print(f"\n🎉 포스팅 성공! 미디어 ID: {media_id}")
            return {"success": True, "media_id": media_id}
        else:
            raise Exception(f"게시 실패: {response.json()}")
    
    def run(self, target_date, count=7, post=False):
        """
        전체 시퀀스 실행
        
        Args:
            target_date: 대상 날짜 (datetime 또는 'YYYY-MM-DD' 문자열)
            count: 동물 수
            post: True면 인스타 포스팅, False면 이미지 생성까지만
        """
        # 날짜 파싱
        if isinstance(target_date, str):
            target_date = datetime.strptime(target_date, '%Y-%m-%d')
        
        print("\n" + "🚀" * 20)
        print(f"   Instagram 자동 포스팅 ({target_date.strftime('%Y-%m-%d')})")
        print("🚀" * 20 + "\n")
        
        try:
            # 1. 동물 데이터 가져오기
            animals = self.fetch_animals(target_date, count)
            
            # 2. 이미지 생성
            image_paths = self.generate_images(animals, target_date)
            
            if not image_paths:
                raise Exception("생성된 이미지가 없습니다.")
            
            # 3. CDN 업로드
            urls = self.upload_to_cdn(image_paths)
            
            if not urls:
                raise Exception("업로드된 이미지가 없습니다.")
            
            # 4. Instagram 포스팅 (post=True일 때만)
            if post:
                result = self.post_to_instagram(urls, animals, target_date)
                
                # 포스팅 성공 시 로컬 이미지 삭제
                if result.get('success'):
                    print("\n🗑️ 로컬 이미지 삭제 중...")
                    for path in image_paths:
                        try:
                            if os.path.exists(path):
                                os.remove(path)
                                print(f"   ✅ 삭제: {os.path.basename(path)}")
                        except Exception as e:
                            print(f"   ⚠️ 삭제 실패: {path} - {e}")
            else:
                print("\n" + "=" * 60)
                print("⏸️  포스팅 대기 (post=True로 실행하면 포스팅)")
                print("=" * 60)
                result = {"success": True, "urls": urls, "posted": False}
            
            print("\n" + "=" * 60)
            print("✅ 완료!")
            print("=" * 60)
            
            return result
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return {"success": False, "error": str(e)}


def main():
    """메인 실행 - 인자로 날짜 받기"""
    import sys
    
    # 환경변수 체크
    required_vars = ["FINDYOU_CDN_TOKEN", "INSTAGRAM_ACCESS_TOKEN"]
    missing = [v for v in required_vars if not os.getenv(v)]
    
    if missing:
        print("❌ 필요한 환경변수:")
        for v in missing:
            print(f"   - {v}")
        return
    
    # 날짜 인자 확인
    if len(sys.argv) < 2:
        print("❌ 사용법: python run_post.py YYYY-MM-DD [--count N] [--post]")
        print("   예시: python run_post.py 2026-01-13")
        print("   예시: python run_post.py 2026-01-13 --count 5 --post")
        return
    
    target_date = sys.argv[1]
    post = "--post" in sys.argv
    
    # --count 옵션 파싱
    count = 7  # 기본값 7 (서울 1 + 경기 1 + 랜덤 5)
    if "--count" in sys.argv:
        try:
            idx = sys.argv.index("--count")
            count = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            pass
    
    # 실행
    poster = InstagramAutoPost()
    result = poster.run(target_date=target_date, count=count, post=post)
    
    if result['success']:
        if result.get('posted', True):
            print("\n🎉 Instagram 포스팅 완료!")
        else:
            print("\n✅ 이미지 생성 및 업로드 완료! (포스팅 안 함)")
    else:
        print(f"\n❌ 실패: {result.get('error')}")


if __name__ == "__main__":
    main()
