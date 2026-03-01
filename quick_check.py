import requests
import json
from datetime import datetime

API_KEY = "AIzaSyBT8d7IfaHjgUglHmarAjnarNLbROZ_hoc"

def get_price(symbol):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    params = {"key": API_KEY}
    payload = {
        "contents": [{
            "parts": [{"text": f"{symbol} stock price change percent February 26 2026"}]
        }],
        "tools": [{"googleSearch": {}}]
    }
    try:
        resp = requests.post(url, params=params, json=payload, timeout=30)
        data = resp.json()
        candidates = data.get('candidates', [])
        if candidates:
            return candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')[:200]
    except:
        pass
    return "获取失败"

stocks = ['SPY', 'QQQ', 'BABA', 'TSLA', 'NVDA']
results = {}

print(f"美股监控 - {datetime.now().strftime('%H:%M:%S')}\n")
for s in stocks:
    print(f"获取 {s}...", flush=True)
    results[s] = get_price(s)
    print(f"  ✓ {s}: {results[s][:80]}...")

print(f"\n检查完成 - {datetime.now().strftime('%H:%M:%S')}")
