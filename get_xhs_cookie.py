from playwright.sync_api import sync_playwright
import json
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    print("打开小红书...")
    page.goto("https://www.xiaohongshu.com")
    
    print("\n=== 请手动登录小红书 ===")
    print("1. 扫码或手机号登录")
    print("2. 登录成功后，按回车键继续...")
    input()
    
    # 获取所有 cookies
    cookies = context.cookies()
    
    # 转换为 Header String 格式
    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    
    print("\n=== Cookie 已提取 ===")
    print(cookie_str[:200] + "..." if len(cookie_str) > 200 else cookie_str)
    
    # 保存到文件
    with open("xiaohongshu_cookies.txt", "w") as f:
        f.write(cookie_str)
    
    print("\n已保存到 xiaohongshu_cookies.txt")
    print("\n可以关闭浏览器了")
    
    time.sleep(2)
    browser.close()
