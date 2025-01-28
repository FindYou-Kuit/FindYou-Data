import json
import os
import pandas as pd

# 로컬 JSON 파일들이 있는 디렉토리 경로
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트가 있는 폴더
json_dir = os.path.join(base_dir, "json")  # JSON 파일 경로
csv_dir = os.path.join(base_dir, "csv")  # CSV 저장 경로

# CSV 저장 디렉토리가 없으면 생성
os.makedirs(csv_dir, exist_ok=True)

# 저장할 CSV 파일 경로
csv_file = os.path.join(csv_dir, "sigungu_names_with_region.csv")

# JSON 파일명과 한글명 매핑
json_to_korean = {
    "Seoul.json": "서울특별시",
    "Busan.json": "부산광역시",
    "Incheon.json": "인천광역시",
    "Gwangju.json": "광주광역시",
    "Sejong.json": "세종특별자치시",
    "Daejeon.json": "대전광역시",
    "Ulsan.json": "울산광역시",
    "Gyeonggi.json": "경기도",
    "Gangwon.json": "강원특별자치도",
    "Chungbuk.json": "충청북도",
    "Chungnam.json": "충청남도",
    "Jeonbuk.json": "전북특별자치도",
    "Jeonnam.json": "전라남도",
    "Gyeongbuk.json": "경상북도",
    "Gyeongnam.json": "경상남도",
    "Jeju.json": "제주특별자치도"
}

# 데이터를 저장할 리스트
data = []

# JSON 파일들을 순회하며 orgdownNm 추출
for file_name, region_name in json_to_korean.items():
    file_path = os.path.join(json_dir, file_name)
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_name} 파일이 존재하지 않습니다.")
        continue

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                if "orgdownNm" in item:
                    data.append([region_name, item["orgdownNm"]])
    
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# 데이터프레임 생성 및 CSV 저장
if data:
    df = pd.DataFrame(data, columns=["시도명", "구이름"])
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")

    print(f"CSV 파일이 저장되었습니다: {csv_file}")
else:
    print("No valid data found to save.")
