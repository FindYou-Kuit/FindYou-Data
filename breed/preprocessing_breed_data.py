import json
import csv
import os

# 파일 경로 딕셔너리
BREED_FILES = {
    "dog": {"json": "breed/json/dog_breeds.json", "csv": "breed/csv/dog_breeds.csv"},
    "cat": {"json": "breed/json/cat_breeds.json", "csv": "breed/csv/cat_breeds.csv"},
    "extra": {"json": "breed/json/extra_breeds.json", "csv": "breed/csv/extra_breeds.csv"}
}

# 상수 선언
COLUMN_NAME = "Breed Name"

def save_breeds_to_csv(json_file_path, csv_file_path):
    """
    JSON 파일에서 개 또는 고양이 품종(knm)을 추출하여 CSV 파일에 저장합니다.
    
    :param json_file_path: JSON 파일 경로 (str)
    :param csv_file_path: 저장할 CSV 파일 경로 (str)
    """
    # 파일 존재 여부 확인
    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist.")
        return

    try:
        # JSON 파일 읽기
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # knm 속성 추출
        items = data["response"]["body"]["items"]["item"]
        breed_names = [item["knm"] for item in items]

        # CSV 파일 저장
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([COLUMN_NAME])  # 헤더 작성
            for name in breed_names:
                writer.writerow([name])  # 데이터 작성

        print(f"Breed names have been saved to {csv_file_path}")
    except KeyError as e:
        print(f"Error: Missing key in JSON file - {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {json_file_path}: {e}")

# import csv

def print_csv_content(csv_file_path):
    """
    CSV 파일 내용을 출력합니다.
    
    :param csv_file_path: CSV 파일 경로 (str)
    """
    try:
        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f"Error: File {csv_file_path} does not exist.")
    except Exception as e:
        print(f"Error reading CSV file {csv_file_path}: {e}")

# CSV 파일 경로
csv_file_path = "breed/csv/cat_breeds.csv"

# CSV 내용 출력
print_csv_content(csv_file_path)


# 함수 호출
for breed_type, paths in BREED_FILES.items():
    print(f"Processing {breed_type} breeds...")
    save_breeds_to_csv(paths["json"], paths["csv"])
