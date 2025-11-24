"""
구조동물 데이터를 기반으로 인스타그램 피드 이미지를 생성하는 스크립트
"""
import json
import os
from datetime import datetime
from typing import List, Dict
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

class InstagramPostCreator:
    def __init__(self, width: int = 1080, height: int = 1350):
        """
        Instagram 피드 이미지 생성기
        
        Args:
            width: 이미지 너비 (기본값: 1080px)
            height: 이미지 높이 (기본값: 1350px, 4:5 비율)
        """
        self.width = width
        self.height = height
        self.background_color = (255, 255, 255)
        self.text_color = (50, 50, 50)
        self.accent_color = (255, 107, 107)
        
    def download_image(self, url: str) -> Image.Image:
        """
        URL에서 이미지를 다운로드합니다.
        
        Args:
            url: 이미지 URL
            
        Returns:
            PIL Image 객체
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            return img
        except Exception as e:
            print(f"이미지 다운로드 실패 ({url}): {e}")
            # 기본 이미지 반환 (회색 박스)
            img = Image.new('RGB', (400, 400), color=(200, 200, 200))
            return img
    
    def create_single_animal_card(
        self, 
        animal_data: Dict, 
        card_width: int, 
        card_height: int
    ) -> Image.Image:
        """
        개별 동물 카드 이미지를 생성합니다.
        
        Args:
            animal_data: 동물 정보 딕셔너리
            card_width: 카드 너비
            card_height: 카드 높이
            
        Returns:
            카드 이미지
        """
        card = Image.new('RGB', (card_width, card_height), color=self.background_color)
        draw = ImageDraw.Draw(card)
        
        # 이미지 다운로드 및 배치
        image_url = animal_data.get('popfile', '')
        if image_url:
            animal_img = self.download_image(image_url)
            # 이미지 크기 조정 (카드 상단 부분)
            img_height = int(card_height * 0.6)
            animal_img.thumbnail((card_width, img_height))
            
            # 이미지를 중앙에 배치
            x_offset = (card_width - animal_img.width) // 2
            y_offset = 10
            card.paste(animal_img, (x_offset, y_offset))
            text_start_y = y_offset + animal_img.height + 20
        else:
            text_start_y = 50
        
        # 텍스트 정보 추가
        try:
            # 시스템 폰트 사용 (한글 지원)
            font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
            font_medium = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
            font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
        except:
            # 폰트를 찾을 수 없는 경우 기본 폰트 사용
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # 정보 추출
        kind = animal_data.get('kindCd', 'N/A')
        age = animal_data.get('age', 'N/A')
        weight = animal_data.get('weight', 'N/A')
        sex = animal_data.get('sexCd', 'N/A')
        color = animal_data.get('colorCd', 'N/A')
        place = animal_data.get('happenPlace', 'N/A')
        special_mark = animal_data.get('specialMark', '')
        notice_no = animal_data.get('noticeNo', '')
        
        # 성별 한글 변환
        sex_kr = {'M': '수컷', 'F': '암컷', 'Q': '미상'}.get(sex, sex)
        
        # 텍스트 그리기
        y = text_start_y
        line_height = 30
        
        # 품종 (강조)
        draw.text((20, y), f"품종: {kind}", fill=self.accent_color, font=font_large)
        y += line_height + 10
        
        # 기본 정보
        draw.text((20, y), f"나이: {age} | 성별: {sex_kr}", fill=self.text_color, font=font_medium)
        y += line_height
        
        draw.text((20, y), f"몸무게: {weight} | 색상: {color}", fill=self.text_color, font=font_medium)
        y += line_height
        
        # 발견 장소
        if len(place) > 30:
            place = place[:30] + "..."
        draw.text((20, y), f"발견장소: {place}", fill=self.text_color, font=font_small)
        y += line_height
        
        # 특징
        if special_mark and len(special_mark) > 0:
            if len(special_mark) > 40:
                special_mark = special_mark[:40] + "..."
            draw.text((20, y), f"특징: {special_mark}", fill=self.text_color, font=font_small)
            y += line_height
        
        # 공고번호
        draw.text((20, y), f"공고번호: {notice_no}", fill=(100, 100, 100), font=font_small)
        
        return card
    
    def create_feed_image(self, animals: List[Dict]) -> Image.Image:
        """
        여러 동물 정보를 하나의 피드 이미지로 생성합니다.
        
        Args:
            animals: 동물 정보 리스트 (최대 5개)
            
        Returns:
            피드 이미지
        """
        feed = Image.new('RGB', (self.width, self.height), color=self.background_color)
        draw = ImageDraw.Draw(feed)
        
        # 헤더 추가
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 48)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # 제목
        title = "🐾 새로운 가족을 기다립니다"
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((self.width - title_width) // 2, 30), title, fill=self.accent_color, font=title_font)
        
        # 날짜
        today = datetime.now().strftime('%Y년 %m월 %d일')
        date_bbox = draw.textbbox((0, 0), today, font=subtitle_font)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text(((self.width - date_width) // 2, 90), today, fill=self.text_color, font=subtitle_font)
        
        # 구분선
        draw.line([(50, 140), (self.width - 50, 140)], fill=self.accent_color, width=3)
        
        # 동물 카드 배치 (최대 5개)
        card_height = (self.height - 200) // min(len(animals), 5)
        y_offset = 160
        
        for i, animal in enumerate(animals[:5]):
            card = self.create_single_animal_card(
                animal, 
                self.width - 40, 
                card_height - 20
            )
            feed.paste(card, (20, y_offset))
            y_offset += card_height
            
            # 마지막이 아니면 구분선 추가
            if i < min(len(animals), 5) - 1:
                draw.line(
                    [(50, y_offset - 10), (self.width - 50, y_offset - 10)],
                    fill=(200, 200, 200),
                    width=1
                )
        
        return feed
    
    def create_simple_grid(self, animals: List[Dict]) -> Image.Image:
        """
        간단한 그리드 형식의 피드 이미지를 생성합니다.
        5개의 동물 이미지를 그리드로 배치합니다.
        
        Args:
            animals: 동물 정보 리스트
            
        Returns:
            피드 이미지
        """
        feed = Image.new('RGB', (self.width, self.height), color=(250, 250, 250))
        draw = ImageDraw.Draw(feed)
        
        # 헤더
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
            info_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
        
        # 제목 배경
        draw.rectangle([(0, 0), (self.width, 100)], fill=self.accent_color)
        title = "🐾 가족을 찾습니다"
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((self.width - title_width) // 2, 30), title, fill=(255, 255, 255), font=title_font)
        
        # 이미지 그리드 (2x2 + 1)
        margin = 20
        spacing = 10
        img_size = (self.width - 2 * margin - spacing) // 2
        
        positions = [
            (margin, 120),
            (margin + img_size + spacing, 120),
            (margin, 120 + img_size + spacing),
            (margin + img_size + spacing, 120 + img_size + spacing),
            (margin + (img_size + spacing) // 2, 120 + 2 * (img_size + spacing))
        ]
        
        for i, (animal, pos) in enumerate(zip(animals[:5], positions)):
            # 이미지 다운로드
            image_url = animal.get('popfile', '')
            if image_url:
                animal_img = self.download_image(image_url)
                animal_img = animal_img.resize((img_size, img_size))
                feed.paste(animal_img, pos)
                
                # 이미지 테두리
                draw.rectangle(
                    [pos, (pos[0] + img_size, pos[1] + img_size)],
                    outline=self.accent_color,
                    width=3
                )
                
                # 정보 오버레이 (하단)
                overlay_height = 60
                overlay_y = pos[1] + img_size - overlay_height
                draw.rectangle(
                    [(pos[0], overlay_y), (pos[0] + img_size, pos[1] + img_size)],
                    fill=(0, 0, 0, 128)
                )
                
                # 품종 정보
                kind = animal.get('kindCd', 'N/A')
                if len(kind) > 15:
                    kind = kind[:15] + "..."
                draw.text(
                    (pos[0] + 10, overlay_y + 10),
                    kind,
                    fill=(255, 255, 255),
                    font=info_font
                )
                
                # 공고번호
                notice_no = animal.get('noticeNo', '')
                draw.text(
                    (pos[0] + 10, overlay_y + 35),
                    f"No. {notice_no}",
                    fill=(255, 255, 255),
                    font=info_font
                )
        
        return feed


def main():
    # 오늘 날짜의 데이터 파일 읽기
    today = datetime.now().strftime('%Y-%m-%d')
    data_file = os.path.join(
        os.path.dirname(__file__),
        'data',
        today,
        'animals.json'
    )
    
    if not os.path.exists(data_file):
        print(f"데이터 파일을 찾을 수 없습니다: {data_file}")
        print("먼저 fetch_animals.py를 실행하여 데이터를 가져오세요.")
        return
    
    # 데이터 로드
    with open(data_file, 'r', encoding='utf-8') as f:
        animals = json.load(f)
    
    if not animals:
        print("동물 데이터가 비어있습니다.")
        return
    
    # 이미지 생성
    creator = InstagramPostCreator()
    
    # 방법 1: 상세 정보 피드
    # feed_image = creator.create_feed_image(animals)
    
    # 방법 2: 간단한 그리드 (추천)
    feed_image = creator.create_simple_grid(animals)
    
    # 이미지 저장
    output_dir = os.path.join(
        os.path.dirname(__file__),
        'output',
        today
    )
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'instagram_post.png')
    feed_image.save(output_file, quality=95)
    
    print(f"인스타그램 피드 이미지가 생성되었습니다: {output_file}")
    print(f"이미지 크기: {feed_image.size}")


if __name__ == "__main__":
    main()

