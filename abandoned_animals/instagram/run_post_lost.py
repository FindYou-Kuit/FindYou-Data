"""
실종동물 Instagram 자동 포스팅 전체 시퀀스
1. 실종동물 API에서 데이터 가져오기 (일주일 범위)
2. 이미지 생성
3. 이미지 URL 업로드 (FindYou CDN)
4. Instagram 캐러셀 포스팅
"""
import os
import json
import time
import random
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from urllib.parse import unquote
from create_image_lost import LostAnimalImageGenerator

load_dotenv()


class LostAnimalAutoPost:
    def __init__(self):
        # FindYou CDN 설정
        self.cdn_url = os.getenv("FINDYOU_CDN_URL")
        self.cdn_token = os.getenv("FINDYOU_CDN_TOKEN")

        # Instagram 설정
        self.ig_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.ig_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        self.graph_api = "https://graph.facebook.com/v20.0"

        # 이미지 생성기
        self.image_generator = LostAnimalImageGenerator()

        # API 키
        self.api_key = os.getenv('ANIMAL_API_KEY')
        
        # 포스팅 기록 파일
        self.posted_file = os.path.join(os.path.dirname(__file__), 'data', 'posted_lost_animals.json')
        self.posted_ids = self._load_posted_ids()
    
    def _load_posted_ids(self):
        """포스팅한 동물 ID 로드"""
        if os.path.exists(self.posted_file):
            with open(self.posted_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('posted_ids', []))
        return set()
    
    def _save_posted_ids(self):
        """포스팅한 동물 ID 저장"""
        os.makedirs(os.path.dirname(self.posted_file), exist_ok=True)
        with open(self.posted_file, 'w', encoding='utf-8') as f:
            json.dump({
                'posted_ids': list(self.posted_ids),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)
    
    def _get_animal_id(self, animal):
        """동물 고유 ID 생성 (popfile URL 기반)"""
        # popfile URL에서 파일명 추출하여 ID로 사용
        popfile = animal.get('popfile', '')
        if popfile and '/files/' in popfile:
            return popfile.split('/files/')[-1]
        # fallback: 여러 필드 조합
        return f"{animal.get('happenDt', '')}_{animal.get('kindCd', '')}_{animal.get('happenAddr', '')}"
        
    def fetch_lost_animals(self, target_date, count=5):
        """1. 실종동물 데이터 가져오기 (일주일 범위, 랜덤 선택, 중복 제외)"""
        print("=" * 60)
        print(f"1️⃣ 실종동물 데이터 가져오기")
        print("=" * 60)
        
        # 날짜 범위: target_date 포함 일주일 전까지
        end_date = target_date
        start_date = target_date - timedelta(days=6)
        
        bgnde = start_date.strftime('%Y%m%d')
        endde = end_date.strftime('%Y%m%d')
        
        print(f"📅 조회 기간: {bgnde} ~ {endde} (일주일)")
        print(f"📋 이미 포스팅한 동물: {len(self.posted_ids)}마리")
        
        api_url = "https://apis.data.go.kr/1543061/lossInfoService/lossInfo"
        
        # API 키 디코딩 (이중 인코딩 방지)
        decoded_key = unquote(self.api_key)
        
        params = {
            'serviceKey': decoded_key,
            'numOfRows': '1000',
            'pageNo': '1',
            '_type': 'json',
            'bgnde': bgnde,
            'endde': endde
        }
        
        print(f"📡 API 호출: {api_url}")
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data or 'response' not in data:
            raise Exception("실종동물 데이터를 가져올 수 없습니다.")
        
        resp = data['response']
        if 'body' not in resp or 'items' not in resp['body']:
            raise Exception("응답 데이터 구조가 올바르지 않습니다.")
        
        items = resp['body']['items']
        if isinstance(items, dict) and 'item' in items:
            animals = items['item']
        else:
            animals = items if items else []
        
        if isinstance(animals, dict):
            animals = [animals]
        
        total_count = len(animals)
        print(f"📊 API 응답: {total_count}마리 발견")
        
        # 필터링: 이미지 있고 + 이미 포스팅하지 않은 것만
        filtered_animals = []
        for animal in animals:
            popfile = animal.get('popfile', '')
            animal_id = self._get_animal_id(animal)

            # 이미지 URL이 유효하고 + 이미 포스팅하지 않은 경우만
            if popfile and '/files/' in popfile and animal_id not in self.posted_ids:
                # 실제 이미지 접근 가능한지 확인
                try:
                    resp = requests.head(popfile, timeout=5)
                    if resp.status_code != 200:
                        continue
                except Exception:
                    continue
                filtered_animals.append(animal)
        
        print(f"🔍 필터링 후 (이미지 있음 + 미포스팅): {len(filtered_animals)}마리")
        
        # 필드 변환 (kindCd → kindNm, happenPlace → lossPlace 등)
        for animal in filtered_animals:
            animal['kindNm'] = animal.get('kindCd', '')
            animal['lossPlace'] = animal.get('happenPlace', '')
            animal['lossDt'] = animal.get('happenDt', '')[:10].replace('-', '') if animal.get('happenDt') else ''
            animal['_animal_id'] = self._get_animal_id(animal)  # ID 저장
        
        # 랜덤으로 count개 선택
        if len(filtered_animals) > count:
            selected = random.sample(filtered_animals, count)
        else:
            selected = filtered_animals[:count]
        
        print(f"\n🎯 선택된 동물 {len(selected)}마리:")
        for i, animal in enumerate(selected, 1):
            happen_dt = animal.get('happenDt', '')[:10]
            print(f"   {i}. [{happen_dt}] {animal.get('kindNm', 'N/A')} - {animal.get('lossPlace', 'N/A')}")
        
        return selected
    
    def generate_images(self, animals, target_date):
        """2. 이미지 생성"""
        print("\n" + "=" * 60)
        print("2️⃣ 이미지 생성")
        print("=" * 60)
        
        image_paths = []
        output_dir = os.path.join(os.path.dirname(__file__), 'generated_images')
        
        for i, animal in enumerate(animals, 1):
            print(f"\n[{i}/{len(animals)}] {animal.get('kindNm', 'N/A')} 이미지 생성 중...")
            result = self.image_generator.create_image(animal, output_dir, target_date=target_date)
            
            if result['success']:
                image_paths.append(result['path'])
                print(f"   ✅ {result['path']}")
            else:
                print(f"   ❌ 실패: {result.get('error', 'Unknown')}")
        
        return image_paths
    
    def upload_to_cdn(self, image_paths):
        """3. CDN 업로드"""
        print("\n" + "=" * 60)
        print("3️⃣ CDN 업로드")
        print("=" * 60)
        
        image_urls = []
        
        for i, path in enumerate(image_paths, 1):
            print(f"\n[{i}/{len(image_paths)}] 업로드 중: {os.path.basename(path)}")
            
            headers = {"Authorization": f"Bearer {self.cdn_token}"}
            
            with open(path, 'rb') as f:
                files = {'files': (os.path.basename(path), f, 'image/jpeg')}
                response = requests.post(self.cdn_url, headers=headers, files=files)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data', {}).get('urls'):
                    url = data['data']['urls'][0]
                    image_urls.append(url)
                    print(f"   ✅ {url}")
                else:
                    print(f"   ❌ 업로드 실패: {data}")
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
        
        return image_urls
    
    def create_instagram_container(self, image_url, is_carousel_item=True):
        """Instagram 미디어 컨테이너 생성"""
        url = f"{self.graph_api}/{self.ig_account_id}/media"
        params = {
            'image_url': image_url,
            'access_token': self.ig_token,
            'is_carousel_item': str(is_carousel_item).lower()
        }
        
        response = requests.post(url, params=params)
        data = response.json()
        
        if 'id' in data:
            return {'success': True, 'container_id': data['id']}
        return {'success': False, 'error': data}
    
    def create_carousel_container(self, children_ids, caption):
        """캐러셀 컨테이너 생성"""
        url = f"{self.graph_api}/{self.ig_account_id}/media"
        params = {
            'media_type': 'CAROUSEL',
            'children': ','.join(children_ids),
            'caption': caption,
            'access_token': self.ig_token
        }
        
        response = requests.post(url, params=params)
        data = response.json()
        
        if 'id' in data:
            return {'success': True, 'container_id': data['id']}
        return {'success': False, 'error': data}
    
    def publish_media(self, container_id):
        """미디어 게시"""
        url = f"{self.graph_api}/{self.ig_account_id}/media_publish"
        params = {
            'creation_id': container_id,
            'access_token': self.ig_token
        }
        
        response = requests.post(url, params=params)
        data = response.json()
        
        if 'id' in data:
            return {'success': True, 'media_id': data['id']}
        return {'success': False, 'error': data}
    
    def wait_for_container(self, container_id, max_wait=60):
        """컨테이너 준비 대기"""
        url = f"{self.graph_api}/{container_id}"
        params = {
            'fields': 'status_code',
            'access_token': self.ig_token
        }
        
        for _ in range(max_wait // 2):
            response = requests.get(url, params=params)
            data = response.json()
            status = data.get('status_code', '')
            
            if status == 'FINISHED':
                return True
            elif status == 'ERROR':
                return False
            
            time.sleep(2)
        
        return False
    
    def generate_hashtags(self, animals):
        """동물 데이터 기반 해시태그 생성"""
        tags = set()
        
        for animal in animals:
            # 지역
            org_nm = animal.get('orgNm', '')
            if '충청북' in org_nm or '충북' in org_nm:
                tags.add('#충북')
            if '경기' in org_nm:
                tags.add('#경기')
            if '서울' in org_nm:
                tags.add('#서울')
            if '부산' in org_nm:
                tags.add('#부산')
            if '대구' in org_nm:
                tags.add('#대구')
            if '인천' in org_nm:
                tags.add('#인천')
            if '광주' in org_nm:
                tags.add('#광주')
            if '대전' in org_nm:
                tags.add('#대전')
            if '울산' in org_nm:
                tags.add('#울산')
            if '세종' in org_nm:
                tags.add('#세종')
            if '제주' in org_nm:
                tags.add('#제주')
            if '전북' in org_nm or '전라북' in org_nm:
                tags.add('#전북')
            if '전남' in org_nm or '전라남' in org_nm:
                tags.add('#전남')
            if '경북' in org_nm or '경상북' in org_nm:
                tags.add('#경북')
            if '경남' in org_nm or '경상남' in org_nm:
                tags.add('#경남')
            if '충남' in org_nm or '충청남' in org_nm:
                tags.add('#충남')
            if '강원' in org_nm:
                tags.add('#강원')
            
            # 동물 종류
            up_kind = animal.get('upKindNm', '')
            if up_kind == '개':
                tags.add('#강아지')
                tags.add('#실종견')
            elif up_kind == '고양이':
                tags.add('#고양이')
                tags.add('#실종묘')
            
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
        
        # 고정 태그
        fixed_tags = ['#찾아유', '#실종동물', '#잃어버린강아지', '#잃어버린고양이', '#찾아주세요']
        for tag in fixed_tags:
            tags.add(tag)
        
        return ' '.join(sorted(tags))
    
    def create_single_container(self, image_url, caption):
        """단일 이미지 컨테이너 생성"""
        url = f"{self.graph_api}/{self.ig_account_id}/media"
        params = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.ig_token
        }
        
        response = requests.post(url, params=params)
        data = response.json()
        
        if 'id' in data:
            return {'success': True, 'container_id': data['id']}
        return {'success': False, 'error': data}
    
    def post_to_instagram(self, image_urls, animals, target_date):
        """4. Instagram 포스팅"""
        print("\n" + "=" * 60)
        print("4️⃣ Instagram 포스팅")
        print("=" * 60)
        
        # 캡션 생성
        end_date = target_date
        start_date = target_date - timedelta(days=6)
        date_range = f"{start_date.strftime('%m/%d')}~{end_date.strftime('%m/%d')}"
        
        caption = f"🚨 실종동물 찾습니다 ({date_range})\n\n"
        caption += "가족을 찾고 있는 아이들입니다 😢\n"
        if len(image_urls) > 1:
            caption += "👉 스와이프해서 모두 확인해주세요!\n"
        caption += "❤️ 발견하시면 꼭 제보 부탁드려요\n\n"
        caption += "📋 더 많은 실종동물 보기\n"
        caption += "👉 https://www.animal.go.kr/front/awtis/loss/lossList.do\n\n"
        caption += self.generate_hashtags(animals)
        
        print(f"📝 캡션:\n{caption}\n")
        
        # 1개일 때 단일 이미지 포스팅
        if len(image_urls) == 1:
            print("📷 단일 이미지 포스팅...")
            result = self.create_single_container(image_urls[0], caption)
            
            if not result['success']:
                return result
            
            container_id = result['container_id']
            print(f"   ✅ 컨테이너 ID: {container_id}")
            
            print("\n처리 대기 중...")
            if not self.wait_for_container(container_id):
                return {'success': False, 'error': '컨테이너 준비 실패'}
            
            print("\n게시 중...")
            publish_result = self.publish_media(container_id)
            
            if publish_result['success']:
                print(f"   ✅ 게시 완료! 미디어 ID: {publish_result['media_id']}")
            
            return publish_result
        
        # 2개 이상일 때 캐러셀 포스팅
        children_ids = []
        for i, url in enumerate(image_urls, 1):
            print(f"[{i}/{len(image_urls)}] 컨테이너 생성 중...")
            result = self.create_instagram_container(url)
            
            if result['success']:
                container_id = result['container_id']
                print(f"   ✅ ID: {container_id}")
                
                # 컨테이너 준비 대기
                if self.wait_for_container(container_id):
                    children_ids.append(container_id)
                else:
                    print(f"   ⚠️ 컨테이너 준비 실패")
            else:
                print(f"   ❌ 실패: {result['error']}")
        
        if len(children_ids) < 2:
            return {'success': False, 'error': '최소 2개 이미지 필요'}
        
        # 캐러셀 컨테이너 생성
        print("\n캐러셀 컨테이너 생성 중...")
        carousel_result = self.create_carousel_container(children_ids, caption)
        
        if not carousel_result['success']:
            return carousel_result
        
        carousel_id = carousel_result['container_id']
        print(f"   ✅ 캐러셀 ID: {carousel_id}")
        
        # 준비 대기
        print("\n처리 대기 중...")
        if not self.wait_for_container(carousel_id):
            return {'success': False, 'error': '캐러셀 준비 실패'}
        
        # 게시
        print("\n게시 중...")
        publish_result = self.publish_media(carousel_id)
        
        if publish_result['success']:
            print(f"   ✅ 게시 완료! 미디어 ID: {publish_result['media_id']}")
        
        return publish_result
    
    def run(self, target_date_str, do_post=False, count=5):
        """전체 시퀀스 실행"""
        print("\n🚀" * 20)
        print(f"   실종동물 Instagram 자동 포스팅 ({target_date_str})")
        print("🚀" * 20)
        
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
        
        # 1. 데이터 가져오기
        animals = self.fetch_lost_animals(target_date, count=count)
        
        if not animals:
            print("❌ 실종동물 데이터가 없습니다.")
            return False
        
        # 2. 이미지 생성
        image_paths = self.generate_images(animals, target_date)
        
        if not image_paths:
            print("❌ 생성된 이미지가 없습니다.")
            return False
        
        # 3. CDN 업로드
        image_urls = self.upload_to_cdn(image_paths)
        
        if not image_urls:
            print("❌ 업로드된 이미지가 없습니다.")
            return False
        
        # 4. Instagram 포스팅
        if do_post:
            result = self.post_to_instagram(image_urls, animals, target_date)
            if result['success']:
                print("\n🎉 실종동물 Instagram 포스팅 완료!")
                
                # 포스팅 성공 시 ID 저장
                for animal in animals:
                    self.posted_ids.add(animal.get('_animal_id', ''))
                self._save_posted_ids()
                print(f"📝 포스팅 기록 저장 완료 (총 {len(self.posted_ids)}마리)")
                
                # 포스팅 성공 시 로컬 이미지 삭제
                print("\n🗑️ 로컬 이미지 삭제 중...")
                for path in image_paths:
                    try:
                        if os.path.exists(path):
                            os.remove(path)
                            print(f"   ✅ 삭제: {os.path.basename(path)}")
                    except Exception as e:
                        print(f"   ⚠️ 삭제 실패: {path} - {e}")
            else:
                print(f"\n❌ 포스팅 실패: {result.get('error', 'Unknown')}")
                return False
        else:
            print("\n⚠️ --post 플래그가 없어 Instagram에 포스팅하지 않습니다.")
        
        print("\n" + "=" * 60)
        print("✅ 전체 시퀀스 완료!")
        print("=" * 60)
        
        return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='실종동물 Instagram 자동 포스팅')
    parser.add_argument('date', help='날짜 (YYYY-MM-DD)')
    parser.add_argument('--post', action='store_true', help='실제로 Instagram에 포스팅')
    parser.add_argument('--count', type=int, default=5, help='포스팅할 동물 수 (기본: 5)')
    
    args = parser.parse_args()
    
    poster = LostAnimalAutoPost()
    poster.run(args.date, do_post=args.post, count=args.count)


if __name__ == "__main__":
    main()
