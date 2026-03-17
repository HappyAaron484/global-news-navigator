import json
import requests
from datetime import datetime

# 3W 標註
# Who: 資深系統分析師自動化工具
# Where: Global HTTP Standard Check
# When: 2026-03-17

def check_sources():
    json_path = 'data/news_sources.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        sources = json.load(f)

    for item in sources:
        url = item['links']['official_url']
        print(f"Checking {item['media_name']}...")
        
        try:
            # 模擬瀏覽器發出請求，避免被某些媒體封鎖
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            item['status']['http_code'] = response.status_code
            item['status']['is_live'] = response.status_code == 200
        except Exception as e:
            print(f"Error checking {url}: {e}")
            item['status']['http_code'] = 404
            item['status']['is_live'] = False
            
        item['status']['verified_at'] = datetime.utcnow().isoformat() + "Z"

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    check_sources()
