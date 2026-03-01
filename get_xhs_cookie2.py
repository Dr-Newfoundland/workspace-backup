from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    print("打开小红书...")
    page.goto("https://www.xiaohongshu.com")
    
    print("\n=== 请在浏览器中登录小红书 ===")
    print("登录完成后，在此终端按回车键继续...")
    input()
    
    # 获取所有 cookies
    cookies = context.cookies()
    
    # 转换为 Header String 格式
    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    
    # 保存到文件
    with open("/Users/cwj18017295567/.openclaw/workspace/xiaohongshu_cookies.txt", "w") as f:
        f.write(cookie_str)
    
    print("\n✅ Cookie 已保存！")
    print(f"长度: {len(cookie_str)} 字符")
    
    browser.close()
