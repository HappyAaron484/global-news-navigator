import requests
import json
import os
from datetime import datetime

# 3W 標註: Who: Senior Analyst / Where: Automation Script / When: 2026-03-18
def check_sources():
    json_path = 'data/news_sources.json'
    
    # 讀取現有數據
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        url = item['links']['official_url']
        print(f"正在校驗: {item['media_name']} ({url})...")
        
        # 強韌性修正：如果 JSON 中缺少 status，自動初始化
        if 'status' not in item:
            item['status'] = {
                "is_live": False,
                "http_code": 0,
                "verified_at": ""
            }

        try:
            # 設置 10 秒超時，避免腳本卡死
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            item['status']['http_code'] = response.status_code
            item['status']['is_live'] = (response.status_code == 200)
            item['status']['verified_at'] = datetime.utcnow().isoformat() + "Z"
        except Exception as e:
            print(f"無法存取 {url}: {str(e)}")
            item['status']['http_code'] = 0
            item['status']['is_live'] = False
            item['status']['verified_at'] = datetime.utcnow().isoformat() + "Z"

    # 寫回 JSON 檔案
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("數據庫校驗完成。")

if __name__ == "__main__":
    check_sources()
