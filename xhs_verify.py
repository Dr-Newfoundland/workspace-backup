from playwright.sync_api import sync_playwright
import time

# 读取 Cookie
cookie_str = open('/Users/cwj18017295567/.openclaw/workspace/xiaohongshu_cookies.txt').read().strip()

# 解析为 Playwright 格式
cookies = []
for item in cookie_str.split('; '):
    if '=' in item:
        name, value = item.split('=', 1)
        cookies.append({
            'name': name.strip(),
            'value': value.strip(),
            'domain': '.xiaohongshu.com',
            'path': '/',
        })

print(f"加载了 {len(cookies)} 个 Cookie")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    
    # 先访问一下小红书域名，才能设置 Cookie
    page = context.new_page()
    page.goto("https://www.xiaohongshu.com")
    time.sleep(2)
    
    # 清除现有 Cookie 并添加新的
    context.clear_cookies()
    context.add_cookies(cookies)
    
    print("✅ Cookie 已注入，刷新页面...")
    page.reload()
    time.sleep(3)
    
    # 检查登录状态
    try:
        # 查找用户头像或用户名元素
        avatar = page.query_selector('img[class*="avatar"], div[class*="user-avatar"]')
        user_menu = page.query_selector('[class*="user-menu"], [class*="login"]')
        
        if avatar or user_menu:
            print("✅ 检测到登录状态！")
        else:
            print("⚠️ 可能未登录，检查页面...")
            
        # 截图查看状态
        page.screenshot(path='/Users/cwj18017295567/.openclaw/workspace/xhs_login_check.png')
        print("📸 已截图保存到 xhs_login_check.png")
        
    except Exception as e:
        print(f"检查出错: {e}")
    
    print("\n👉 浏览器保持打开，你可以检查登录状态")
    print("   关闭浏览器窗口来结束")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    browser.close()
