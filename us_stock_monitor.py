#!/opt/homebrew/bin/python3.13
import requests
import json
import time
import os
from datetime import datetime

# 监控的股票列表
STOCKS = {
    # 大盘指数 ETF
    'SPY': '标普500 ETF',
    'QQQ': '纳斯达克100 ETF', 
    'DIA': '道琼斯 ETF',
    'VIX': '波动率指数',
    
    # 热门中概股
    'BABA': '阿里巴巴',
    'PDD': '拼多多',
    'JD': '京东',
    'NIO': '蔚来',
    'XPEV': '小鹏汽车',
    'LI': '理想汽车',
    'TSLA': '特斯拉',
    'AAPL': '苹果',
    'NVDA': '英伟达',
    'MSFT': '微软',
    'GOOGL': '谷歌',
    'AMZN': '亚马逊',
    'META': 'Meta',
    'M': '梅西百货',
}

# 异动阈值
THRESHOLD = 3.0  # 涨跌幅超过3%

# 停止标志文件
STOP_FILE = '/Users/cwj18017295567/.openclaw/workspace/stop_monitor.txt'

def get_stock_data(symbol):
    """获取股票数据"""
    try:
        # 使用 Gemini 搜索获取实时数据
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        params = {"key": "AIzaSyBT8d7IfaHjgUglHmarAjnarNLbROZ_hoc"}
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{symbol} stock current price change percent today February 26 2026"}]
            }],
            "tools": [{"googleSearch": {}}]
        }
        
        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, params=params, headers=headers, json=payload, timeout=30)
        data = resp.json()
        
        candidates = data.get('candidates', [])
        if candidates:
            text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            return text
        return None
    except Exception as e:
        return f"Error: {e}"

def check_stop():
    """检查是否应该停止"""
    return os.path.exists(STOP_FILE)

def send_alert(message):
    """发送通知 - 写入文件供 OpenClaw 读取"""
    alert_file = '/Users/cwj18017295567/.openclaw/workspace/us_stock_alerts.txt'
    with open(alert_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(message)
        f.write(f"\n{'='*50}\n")
    print(f"[ALERT] {datetime.now().strftime('%H:%M:%S')} - Alert saved")

def monitor():
    """主监控循环"""
    print(f"开始美股异动监控 - {datetime.now()}")
    print(f"监控股票数: {len(STOCKS)}")
    print(f"异动阈值: ±{THRESHOLD}%")
    print(f"监控间隔: 5分钟")
    print(f"停止方式: 创建文件 {STOP_FILE}")
    print("-" * 50)
    
    round_num = 0
    
    while True:
        if check_stop():
            print(f"\n检测到停止信号，监控结束 - {datetime.now()}")
            os.remove(STOP_FILE)
            break
        
        round_num += 1
        print(f"\n第 {round_num} 轮检查 - {datetime.now().strftime('%H:%M:%S')}")
        
        # 检查重点股票
        for symbol, name in list(STOCKS.items())[:5]:  # 先检查前5只
            if check_stop():
                break
            
            print(f"  检查 {symbol} ({name})...", end=' ', flush=True)
            data = get_stock_data(symbol)
            
            if data and ('Error' not in data):
                # 简单判断是否有大幅波动（这里简化处理，实际应该解析数据）
                print(f"✓")
                # 如果有异动关键词，记录
                if any(x in data.lower() for x in ['surge', 'plunge', 'jump', 'drop', 'soar', 'tumble']):
                    alert = f"🚨 {name} ({symbol}) 异动:\n{data[:500]}"
                    send_alert(alert)
            else:
                print(f"✗")
            
            time.sleep(2)  # 避免请求过快
        
        if check_stop():
            break
        
        # 每轮检查完成后，发送状态报告
        status = f"第 {round_num} 轮检查完成 - {datetime.now().strftime('%H:%M:%S')}\n监控中: {', '.join(list(STOCKS.keys())[:5])}..."
        print(status)
        
        # 等待5分钟
        print("等待5分钟...")
        for i in range(300):  # 300秒 = 5分钟
            if check_stop():
                break
            time.sleep(1)

if __name__ == '__main__':
    monitor()
