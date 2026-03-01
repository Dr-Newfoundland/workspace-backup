import requests
import json

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
params = {"key": "AIzaSyBT8d7IfaHjgUglHmarAjnarNLbROZ_hoc"}

payload = {
    "contents": [{
        "parts": [{"text": "Macy's stock M NYSE current price today February 26 2026"}]
    }],
    "tools": [{"googleSearch": {}}]
}

headers = {"Content-Type": "application/json"}

resp = requests.post(url, params=params, headers=headers, json=payload)
data = resp.json()

candidates = data.get('candidates', [])
if candidates:
    text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
    print(text)
else:
    print('Error:', data.get('error', {}).get('message', 'Unknown error'))
