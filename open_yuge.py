from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print("打开雨哥 B 站空间...")
    page.goto("https://space.bilibili.com/194742412/video?tid=0&page=1&keyword=&order=pubdate")
    
    print("\n页面已加载，请查看浏览器中的最新视频")
    print("关闭浏览器窗口来结束")
    
    # 保持浏览器打开
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    browser.close()
