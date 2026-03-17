import requests
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime

# 3W: Who: Senior Analyst | Where: RSS & Status Maintainer | When: 2026-03-18

def get_rss_headlines():
    # 預設追蹤 3 個 RSS 源
    feeds = {
        "Reuters": "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best",
        "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "CNA 中央社": "https://feeds.feedburner.com/cnaFirstNews"
    }
    
    headlines = []
    print("正在抓取 RSS 即時頭條...")
    
    for source, url in feeds.items():
        try:
            resp = requests.get(url, timeout=10)
            root = ET.fromstring(resp.content)
            # 解析 RSS 2.0 格式
            for item in root.findall('./channel/item')[:5]: # 每個來源取前 5 則
                title = item.find('title').text
                headlines.append(f"[{source}] {title}")
        except Exception as e:
            print(f"RSS 抓取失敗 ({source}): {e}")
            
    return headlines

def check_sources():
    json_path = 'data/news_sources.json'
    ticker_path = 'data/ticker.json'
    
    # 1. 執行 RSS 抓取
    headlines = get_rss_headlines()
    with open(ticker_path, 'w', encoding='utf-8') as f:
        json.dump({"headlines": headlines, "updated_at": datetime.utcnow().isoformat()}, f, ensure_ascii=False)

    # 2. 執行 40 筆媒體狀態校驗
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        url = item['links']['official_url']
        if 'status' not in item:
            item['status'] = {"is_live": False, "http_code": 0, "verified_at": ""}
        
        try:
            resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            item['status']['http_code'] = resp.status_code
            item['status']['is_live'] = (resp.status_code == 200)
            item['status']['verified_at'] = datetime.utcnow().isoformat() + "Z"
        except:
            item['status']['is_live'] = False
            item['status']['verified_at'] = datetime.utcnow().isoformat() + "Z"

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("維護任務完成。")

if __name__ == "__main__":
    check_sources()
