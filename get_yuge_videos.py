from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    print("打开雨哥 B 站空间...")
    page.goto("https://space.bilibili.com/194742412/video")
    
    page.wait_for_timeout(3000)
    
    # 获取视频列表
    videos = page.query_selector_all('.small-item')
    
    print(f"\n找到 {len(videos)} 个视频\n")
    
    results = []
    for i, video in enumerate(videos[:5]):
        try:
            title_elem = video.query_selector('.title')
            title = title_elem.inner_text() if title_elem else 'N/A'
            
            time_elem = video.query_selector('.time')
            pub_time = time_elem.inner_text() if time_elem else 'N/A'
            
            # 获取时长
            duration_elem = video.query_selector('.length')
            duration = duration_elem.inner_text() if duration_elem else 'N/A'
            
            link_elem = video.query_selector('a')
            href = link_elem.get_attribute('href') if link_elem else ''
            
            results.append({
                'title': title,
                'time': pub_time,
                'duration': duration,
                'link': f"https:{href}" if href.startswith('//') else href
            })
            
            print(f"{i+1}. {title}")
            print(f"   时长: {duration}")
            print(f"   发布时间: {pub_time}")
            print()
        except Exception as e:
            print(f"解析出错: {e}")
    
    # 保存结果
    with open('/Users/cwj18017295567/.openclaw/workspace/yuge_videos.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("按 Enter 关闭浏览器...")
    input()
    browser.close()
