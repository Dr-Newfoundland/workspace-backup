#!/usr/bin/env python3
"""小红书 Cookie 工具 - 用保存的 Cookie 访问小红书内容"""

import requests
import json
import sys

# 读取 Cookie
with open("/Users/cwj18017295567/.openclaw/workspace/xiaohongshu_cookies.txt", "r") as f:
    COOKIE = f.read().strip()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Referer": "https://www.xiaohongshu.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def search_xhs(keyword, num=10):
    """搜索小红书笔记"""
    url = "https://www.xiaohongshu.com/api/sns/web/v1/search/notes"
    params = {
        "keyword": keyword,
        "page": 1,
        "page_size": num,
        "sort": "general",
    }
    
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def get_note_detail(note_id):
    """获取笔记详情"""
    url = f"https://www.xiaohongshu.com/api/sns/web/v1/feed/{note_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def test_login():
    """测试 Cookie 是否有效"""
    url = "https://www.xiaohongshu.com/api/sns/web/v1/user/selfinfo"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    
    if data.get("success"):
        user = data.get("data", {})
        print(f"✅ Cookie 有效！")
        print(f"用户: {user.get('nickname', 'Unknown')}")
        print(f"ID: {user.get('id', 'Unknown')}")
        return True
    else:
        print(f"❌ Cookie 无效或已过期")
        print(f"错误: {data.get('msg', 'Unknown error')}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print(f"  {sys.argv[0]} test          # 测试 Cookie 是否有效")
        print(f"  {sys.argv[0]} search 关键词   # 搜索笔记")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "test":
        test_login()
    elif cmd == "search" and len(sys.argv) >= 3:
        keyword = sys.argv[2]
        result = search_xhs(keyword)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("未知命令")
