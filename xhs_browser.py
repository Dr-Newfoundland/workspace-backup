from playwright.sync_api import sync_playwright
import time

# 读取 Cookie
with open('/Users/cwj18017295567/.openclaw/workspace/xiaohongshu_cookies.txt', 'r') as f:
    cookie_str = f.read().strip()

cookies_list = []
for item in cookie_str.split('; '):
    if '=' in item:
        name, value = item.split('=', 1)
        cookies_list.append({
            'name': name,
            'value': value,
            'domain': '.xiaohongshu.com',
            'path': '/'
        })

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    
    # 添加 cookies
    context.add_cookies(cookies_list)
    
    page = context.new_page()
    
    print("✅ 使用 Cookie 打开小红书...")
    page.goto("https://www.xiaohongshu.com")
    
    print("\n👉 检查是否已登录...")
    time.sleep(3)
    
    # 检查页面是否显示用户信息
    try:
        # 等待页面加载
        page.wait_for_selector("[class*='avatar']", timeout=10000)
        print("✅ 应该已登录！")
    except:
        print("⚠️ 可能需要刷新或 Cookie 已过期")
    
    print("\n👉 你可以现在：")
    print("1. 搜索想看的内容")
    print("2. 浏览笔记")
    print("3. 关闭浏览器窗口来结束")
    
    # 保持浏览器打开
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    browser.close()
    print("\n✅ 浏览器已关闭")
