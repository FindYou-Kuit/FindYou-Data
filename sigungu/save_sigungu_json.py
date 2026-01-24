import requests
import json
import os

# Service Key from environment variable
service_key = os.getenv('PUBLIC_DATA_API_KEY')
if not service_key:
    raise Exception("PUBLIC_DATA_API_KEY 환경변수가 필요합니다.")

# Base URL for the GET request
base_url = f"http://apis.data.go.kr/1543061/abandonmentPublicSrvc/sigungu?serviceKey={service_key}"

# Mapping of upr_cd to filenames
codes_and_files = {
    "6110000": "Seoul.json",
    "6260000": "Busan.json",
    "6280000": "Incheon.json",
    "6290000": "Gwangju.json",
    "5690000": "Sejong.json",
    "6300000": "Daejeon.json",
    "6310000": "Ulsan.json",
    "6410000": "Gyeonggi.json",
    "6530000": "Gangwon.json",
    "6430000": "Chungbuk.json",
    "6440000": "Chungnam.json",
    "6540000": "Jeonbuk.json",
    "6460000": "Jeonnam.json",
    "6470000": "Gyeongbuk.json",
    "6480000": "Gyeongnam.json",
    "6500000": "Jeju.json"
}

# Iterate over each upr_cd and save the corresponding JSON
for upr_cd, filename in codes_and_files.items():
    params = {
        "upr_cd": upr_cd,
        "_type": "json"
    }

    # Send the GET request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Parse the JSON response
            response_json = response.json()
            
            # Extract the 'items' part
            items = response_json.get('response', {}).get('body', {}).get('items', {}).get('item', [])

            # Save the items to a JSON file
            with open(f"{filename}", "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=4)

            print(f"Saved data for upr_cd {upr_cd} to {filename}")

        except json.JSONDecodeError as e:
            print(f"JSON decode error for upr_cd {upr_cd}: {e}")
        except Exception as e:
            print(f"Error processing upr_cd {upr_cd}: {e}")
    else:
        print(f"Failed to fetch data for upr_cd {upr_cd}: {response.status_code}, {response.content}")
