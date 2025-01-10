import json
import os

def extract_knm_to_json(input_json_path, output_json_path):
    """
    원시 JSON 데이터에서 'knm' 필드만 추출하여 새로운 JSON 파일로 저장합니다.
    
    :param input_json_path: 원시 JSON 파일 경로 (str)
    :param output_json_path: 추출된 JSON 파일 경로 (str)
    """
    try:
        # JSON 파일 읽기
        with open(input_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 'knm' 필드만 추출
        items = data["response"]["body"]["items"]["item"]
        knm_list = [{"knm": item["knm"]} for item in items]

        # 추출된 데이터를 새로운 JSON 파일로 저장
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(knm_list, f, ensure_ascii=False, indent=4)

        print(f"'knm' data has been saved to {output_json_path}")
    except FileNotFoundError:
        print(f"Error: File {input_json_path} does not exist.")
    except KeyError as e:
        print(f"Error: Missing key in JSON data - {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {input_json_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# 파일 경로 딕셔너리
BREED_FILES = {
    "dog": {
        "input_json": "breed/open-api-response/dog_breeds.json",
        "output_json": "breed/json/dog_breeds.json"
    },
    "cat": {
        "input_json": "breed/open-api-response/cat_breeds.json",
        "output_json": "breed/json/cat_breeds.json"
    },
    "extra": {
        "input_json": "breed/open-api-response/extra_breeds.json",
        "output_json": "breed/json/extra_breeds.json"
    }
}

# 각 파일 처리
for breed_type, paths in BREED_FILES.items():
    print(f"Processing {breed_type} breeds...")
    extract_knm_to_json(paths["input_json"], paths["output_json"])
