from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    print("✅ 浏览器已打开")
    page.goto("https://www.xiaohongshu.com")
    print("\n👉 请在小红书网页版登录")
    print("👉 登录完成后，直接关闭浏览器窗口")
    print("👉 Cookie 会自动保存\n")
    
    # 等待浏览器被关闭
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # 获取 cookies
    cookies = context.cookies()
    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    
    with open("/Users/cwj18017295567/.openclaw/workspace/xiaohongshu_cookies.txt", "w") as f:
        f.write(cookie_str)
    
    print(f"\n✅ Cookie 已保存！({len(cookie_str)} 字符)")
    browser.close()
