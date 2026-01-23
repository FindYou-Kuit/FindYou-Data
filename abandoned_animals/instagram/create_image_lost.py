"""
실종동물 인스타그램 포스트 JPG 이미지 생성
"""
import os
import time
import json
import base64
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class LostAnimalImageGenerator:
    def __init__(self):
        self.canvas_width = 1080
        self.canvas_height = 1500

    def generate_html(self, animal_data, target_date=None):
        """HTML 템플릿 생성"""
        # 날짜 설정
        if target_date:
            notice_date = target_date
        else:
            # lossInfo API의 날짜 필드 사용
            loss_dt = animal_data.get('lossDt', '')
            if loss_dt and len(loss_dt) == 8:
                notice_date = datetime.strptime(loss_dt, '%Y%m%d')
            else:
                notice_date = datetime.now()
        
        weekdays_kr = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        weekday_kr = weekdays_kr[notice_date.weekday()]
        title_text = f"{notice_date.strftime('%Y-%m-%d')} {weekday_kr} 실종동물 공고"

        # 동물 정보 추출
        breed_text = animal_data.get('kindNm', '믹스견')
        sex_text = {'M': '수컷', 'F': '암컷', 'Q': '미상'}.get(animal_data.get('sexCd', 'Q'), '미상')
        
        # 실종지역 (시/군/구)
        loss_place = animal_data.get('lossPlace', 'N/A')
        
        # 실종주소 (상세주소)
        org_nm = animal_data.get('orgNm', '')  # 예: 경기도 양주시
        full_address = f"{org_nm} {loss_place}" if org_nm else loss_place
        
        # 특징
        special_mark = animal_data.get('specialMark', '정보 없음')
        
        # 이미지 URL
        image_url = animal_data.get('popfile', '') or animal_data.get('popfile1', '')

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

        # 포스트잇 가운데 정렬: (1080 - 612) / 2 = 234
        polaroid_left = 234

        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>실종동물 공고</title>
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
            background: linear-gradient(180deg, #FFDCD9 0%, #FFEFEE 100%);
        }}

        .polaroid-frame {{
            position: absolute;
            width: 612px;
            height: 689px;
            left: {polaroid_left}px;
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
            width: 532px;
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
            width: 768px;
            height: 70px;
            left: 156px;
            top: 63px;
            font-family: 'Jua', sans-serif;
            font-style: normal;
            font-weight: 400;
            font-size: 56px;
            line-height: 70px;
            text-align: center;
            color: #2C2B2B;
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

        .sex-label {{ position: absolute; left: 105px; top: 967px; }}
        .sex-value {{ position: absolute; left: 304px; top: 967px; }}
        .place-label {{ position: absolute; left: 105px; top: 1046px; }}
        .place-value {{ position: absolute; left: 304px; top: 1046px; }}
        .address-label {{ position: absolute; left: 105px; top: 1125px; }}
        .address-value {{ position: absolute; width: 700px; left: 304px; top: 1125px; font-size: 40px !important; }}
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
                <img src="{image_url}" alt="실종동물 사진" onerror="this.style.display='none'">
            </div>
            <div class="breed-name">{breed_text}</div>
        </div>

        <div class="title">{title_text}</div>

        <div class="sex-label label">성별</div>
        <div class="sex-value value">{sex_text}</div>

        <div class="place-label label">실종지역</div>
        <div class="place-value value">{loss_place}</div>

        <div class="address-label label">실종주소</div>
        <div class="address-value value">{full_address}</div>

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
        print("🚀 실종동물 이미지 생성 시작...")

        os.makedirs(output_dir, exist_ok=True)

        html_content = self.generate_html(animal_data, target_date)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        jpg_path = os.path.join(output_dir, f"lost_animal_{timestamp}.jpg")

        driver = None
        try:
            print("🌐 WebDriver 설정 중...")
            driver = self.setup_driver()

            html_base64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
            driver.get(f"data:text/html;base64,{html_base64}")

            print("⏳ 페이지 및 폰트 로딩 대기 중...")
            time.sleep(2)
            
            # 웹폰트 로딩 대기
            driver.execute_script("""
                return new Promise((resolve) => {
                    if (document.fonts && document.fonts.ready) {
                        document.fonts.ready.then(() => resolve());
                    } else {
                        resolve();
                    }
                });
            """)
            time.sleep(3)

            driver.execute_script(f"""
                document.body.style.overflow = 'hidden';
                document.documentElement.style.overflow = 'hidden';
                document.body.style.margin = '0';
                document.body.style.padding = '0';
                document.body.style.width = '{self.canvas_width}px';
                document.body.style.height = '{self.canvas_height}px';
            """)

            print(f"📸 {self.canvas_width}x{self.canvas_height} 스크린샷 생성 중...")
            temp_png = jpg_path.replace('.jpg', '_temp.png')
            driver.save_screenshot(temp_png)

            print("🔄 JPG 변환 중...")
            self._convert_to_jpg(temp_png, jpg_path)

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


def main():
    """테스트용 메인"""
    # 테스트 데이터
    test_data = {
        'kindNm': '진도견',
        'sexCd': 'F',
        'lossPlace': '공장지대',
        'orgNm': '경기도 양주시 백석읍 중앙로 33',
        'specialMark': '공장에서 키우는 진도개인데 목줄을 끊고 없어졌어요ㅠ',
        'popfile': 'https://www.animal.go.kr/files/shelter/2026/01/202601121401514_s.jpg'
    }
    
    generator = LostAnimalImageGenerator()
    target_date = datetime(2026, 1, 12)
    result = generator.create_image(test_data, target_date=target_date)
    
    if result['success']:
        print(f"✅ 생성 완료: {result['path']}")
        os.system(f"open {result['path']}")


if __name__ == "__main__":
    main()
