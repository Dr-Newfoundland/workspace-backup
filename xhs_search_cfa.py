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
    
    print("🔍 在小红书搜索 CFA 考试...")
    
    # 访问小红书搜索页
    page.goto("https://www.xiaohongshu.com/search_result?keyword=CFA%E8%80%83%E8%AF%95%E5%87%86%E5%A4%87")
    
    # 等待页面加载
    time.sleep(5)
    
    # 滚动页面加载更多内容
    for i in range(3):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(2)
    
    # 提取笔记信息
    notes = page.query_selector_all('[class*="note-item"], [class*="feed-item"]')
    
    results = []
    for note in notes[:10]:
        try:
            title = note.query_selector('[class*="title"]').inner_text()
            desc = note.query_selector('[class*="desc"]').inner_text()
            author = note.query_selector('[class*="author"]').inner_text()
            results.append({
                'title': title,
                'desc': desc,
                'author': author
            })
        except:
            pass
    
    print(f"\n✅ 找到 {len(results)} 篇相关笔记\n")
    
    for i, r in enumerate(results[:5], 1):
        print(f"{i}. {r.get('title', '无标题')}")
        print(f"   作者: {r.get('author', '未知')}")
        print(f"   摘要: {r.get('desc', '无摘要')[:100]}...")
        print()
    
    # 保存完整结果
    import json
    with open('/Users/cwj18017295567/.openclaw/workspace/xhs_cfa_search.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("💡 浏览器保持打开，你可以继续浏览")
    print("   按 Ctrl+C 结束或直接关闭浏览器")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    browser.close()
