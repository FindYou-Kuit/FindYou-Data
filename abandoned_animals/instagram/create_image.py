"""
수집된 동물 데이터로 인스타그램 포스트 JPG 이미지 생성
HTML 파일 저장 없이 바로 이미지로 변환
"""
import os
import time
import json
import base64
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class ImageGenerator:
    def __init__(self):
        self.canvas_width = 1080
        self.canvas_height = 1500

    def generate_html(self, animal_data, target_date=None):
        """HTML 템플릿 생성 (메모리에서만 사용)"""
        # 공고일 기준으로 날짜 설정 (noticeSdt: 20260113 형식)
        if target_date:
            notice_date = target_date
        else:
            notice_sdt = animal_data.get('noticeSdt', '')
            if notice_sdt and len(notice_sdt) == 8:
                notice_date = datetime.strptime(notice_sdt, '%Y%m%d')
            else:
                notice_date = datetime.now()
        
        weekdays_kr = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        weekday_kr = weekdays_kr[notice_date.weekday()]
        title_text = f"{notice_date.strftime('%Y-%m-%d')} {weekday_kr} 보호동물 공고"

        # 동물 정보 추출
        breed_text = animal_data.get('kindNm', '믹스견')
        notice_number = animal_data.get('noticeNo', 'N/A')
        sex_text = {'M': '수컷', 'F': '암컷', 'Q': '미상'}.get(animal_data.get('sexCd', 'Q'), '미상')
        care_name = animal_data.get('careNm', 'N/A')
        special_mark = animal_data.get('specialMark', '정보 없음')
        image_url = animal_data.get('popfile1', '')

        # 텍스트 길이에 따라 폰트 사이즈 결정
        text_length = len(special_mark)
        if text_length < 30:
            font_size = 48
        elif text_length < 50:
            font_size = 42
        elif text_length < 70:
            font_size = 36
        else:
            font_size = 32

        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>보호동물 공고</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Jua:wght@400&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
        
        @font-face {{
            font-family: 'BMHANNAAir';
            src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_four@1.0/BMHANNAAir.woff') format('woff');
            font-weight: normal;
            font-style: normal;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html, body {{
            overflow: hidden;
            margin: 0;
            padding: 0;
            width: {self.canvas_width}px;
            height: {self.canvas_height}px;
        }}

        .main-container {{
            position: relative;
            width: {self.canvas_width}px;
            height: {self.canvas_height}px;
            background: linear-gradient(180deg, #FFD195 0%, #FFEED9 100%);
        }}

        .polaroid-frame {{
            position: absolute;
            width: 612.06px;
            height: 689.28px;
            left: 205px;
            top: 180px;
            transform: rotate(5deg);
            z-index: 1;
        }}

        .polaroid-bg {{
            position: absolute;
            width: 100%;
            height: 100%;
            left: 0;
            top: 0;
            background: #F5F5F5;
            box-shadow: 10px 10px 4px rgba(0, 0, 0, 0.25);
        }}

        .animal-photo {{
            position: absolute;
            width: 532.02px;
            height: 528px;
            left: 40px;
            top: 34px;
            overflow: hidden;
            z-index: 2;
        }}

        .animal-photo img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: center;
        }}

        .title {{
            position: absolute;
            width: 100%;
            height: 70px;
            left: 0;
            top: 63px;
            font-family: 'Jua', sans-serif;
            font-style: normal;
            font-weight: 400;
            font-size: 56px;
            line-height: 70px;
            text-align: center;
            color: #2C2B2B;
            white-space: nowrap;
        }}

        .label {{
            font-family: 'Jua', sans-serif;
            font-style: normal;
            font-weight: 400;
            font-size: 48px;
            line-height: 49px;
            color: #2C2B2B;
            white-space: nowrap;
        }}

        .value {{
            font-family: 'BMHANNAAir', sans-serif;
            font-style: normal;
            font-weight: 400;
            font-size: 48px;
            line-height: 49px;
            color: #2C2B2B;
            white-space: nowrap;
        }}

        .notice-label {{ position: absolute; left: 105px; top: 967px; }}
        .notice-value {{ position: absolute; left: 304px; top: 967px; }}
        .sex-label {{ position: absolute; left: 105px; top: 1046px; }}
        .sex-value {{ position: absolute; left: 304px; top: 1046px; }}
        .center-label {{ position: absolute; left: 105px; top: 1125px; }}
        .center-value {{ position: absolute; width: 657px; left: 304px; top: 1125px; }}
        .feature-label {{ position: absolute; left: 105px; top: 1204px; }}
        .feature-value {{
            position: absolute;
            width: 657px;
            max-height: 196px;
            left: 304px;
            top: 1204px;
            font-family: 'BMHANNAAir', sans-serif;
            font-style: normal;
            font-weight: 400;
            color: #2C2B2B;
            overflow: hidden;
            white-space: pre-line;
            word-break: break-all;
        }}

        .breed-name {{
            position: absolute;
            left: 50%;
            bottom: 40px;
            transform: translateX(-50%);
            font-family: 'Jua', sans-serif;
            font-size: 42px;
            text-align: center;
            color: #2C2B2B;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
            z-index: 3;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="polaroid-frame">
            <div class="polaroid-bg"></div>
            <div class="animal-photo">
                <img src="{image_url}" alt="구조동물 사진" onerror="this.style.display='none'">
            </div>
            <div class="breed-name">{breed_text}</div>
        </div>

        <div class="title">{title_text}</div>

        <div class="notice-label label">공고번호</div>
        <div class="notice-value value">{notice_number}</div>

        <div class="sex-label label">성별</div>
        <div class="sex-value value">{sex_text}</div>

        <div class="center-label label">보호센터</div>
        <div class="center-value value">{care_name}</div>

        <div class="feature-label label">특징</div>
        <div class="feature-value value" style="font-size: {font_size}px !important; line-height: {int(font_size * 1.02)}px !important;">{special_mark}</div>
    </div>
</body>
</html>"""

        return html_content

    def setup_driver(self):
        """Chrome WebDriver 설정"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument(f'--window-size={self.canvas_width},{self.canvas_height}')
        chrome_options.add_argument('--force-device-scale-factor=2')

        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            driver = webdriver.Chrome(options=chrome_options)

        driver.set_window_size(self.canvas_width, self.canvas_height)
        return driver

    def create_image(self, animal_data, output_dir="generated_images", target_date=None):
        """동물 데이터로 JPG 이미지 생성"""
        print("🚀 이미지 생성 시작...")

        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)

        # HTML 생성 (메모리에서만)
        html_content = self.generate_html(animal_data, target_date)

        # 파일명 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        jpg_path = os.path.join(output_dir, f"animal_post_{timestamp}.jpg")

        driver = None
        try:
            print("🌐 WebDriver 설정 중...")
            driver = self.setup_driver()

            # HTML을 data URI로 로드 (파일 저장 없이)
            html_base64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
            driver.get(f"data:text/html;base64,{html_base64}")

            # 폰트 로딩 대기
            print("⏳ 페이지 로딩 대기 중...")
            time.sleep(3)

            # 스크롤바 숨기기
            driver.execute_script(f"""
                document.body.style.overflow = 'hidden';
                document.documentElement.style.overflow = 'hidden';
                document.body.style.margin = '0';
                document.body.style.padding = '0';
                document.body.style.width = '{self.canvas_width}px';
                document.body.style.height = '{self.canvas_height}px';
            """)

            # 임시 PNG 스크린샷
            print(f"📸 {self.canvas_width}x{self.canvas_height} 스크린샷 생성 중...")
            temp_png = jpg_path.replace('.jpg', '_temp.png')
            driver.save_screenshot(temp_png)

            # PNG → JPG 변환
            print("🔄 JPG 변환 중...")
            self._convert_to_jpg(temp_png, jpg_path)

            # 임시 파일 삭제
            if os.path.exists(temp_png):
                os.remove(temp_png)

            print(f"🎉 이미지 생성 완료: {jpg_path}")
            return {'path': jpg_path, 'success': True}

        except Exception as e:
            print(f"❌ 오류: {e}")
            return {'error': str(e), 'success': False}
        finally:
            if driver:
                driver.quit()

    def _convert_to_jpg(self, png_path, jpg_path):
        """PNG를 JPG로 변환"""
        from PIL import Image

        with Image.open(png_path) as img:
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            img.save(jpg_path, 'JPEG', quality=95, optimize=True)


def main(animal_index=2):
    """메인 실행 함수"""
    print("🐾 동물 데이터로 이미지 생성")
    print("=" * 50)

    # 오늘 날짜 데이터 파일 찾기
    today = datetime.now().strftime('%Y-%m-%d')
    data_file = f"data/{today}/animals.json"

    if not os.path.exists(data_file):
        print(f"❌ 데이터 파일 없음: {data_file}")
        print("💡 먼저 python fetch_animals.py 실행")
        return None

    with open(data_file, 'r', encoding='utf-8') as f:
        animals = json.load(f)

    if not animals:
        print("❌ 동물 데이터가 없습니다.")
        return None

    if animal_index >= len(animals):
        animal_index = 0

    selected = animals[animal_index]
    print(f"✅ {animal_index + 1}번 동물 선택:")
    print(f"   품종: {selected.get('kindNm', 'N/A')} ({selected.get('sexCd', 'N/A')})")
    print(f"   보호센터: {selected.get('careNm', 'N/A')}")
    print(f"   특징: {selected.get('specialMark', 'N/A')}")
    print()

    # 이미지 생성
    generator = ImageGenerator()
    result = generator.create_image(selected)

    if result['success']:
        print("\n" + "=" * 50)
        print(f"📸 JPG: {result['path']}")
        print("=" * 50)
        return result['path']
    else:
        print(f"\n❌ 실패: {result.get('error')}")
        return None


if __name__ == "__main__":
    main()




