#!/opt/homebrew/bin/python3.13
"""贵金属及有色金属实时监控脚本 - 雅虎财经版"""
import requests
import json
from datetime import datetime, timezone, timedelta
import os
import yfinance as yf

# 雅虎财经代码映射
YAHOO_SYMBOLS = {
    # 贵金属
    'GC=F': {'name': '黄金', 'unit': '美元/盎司', 'yahoo': 'GC=F'},
    'SI=F': {'name': '白银', 'unit': '美元/盎司', 'yahoo': 'SI=F'},
    'PL=F': {'name': '铂金', 'unit': '美元/盎司', 'yahoo': 'PL=F'},
    'PA=F': {'name': '钯金', 'unit': '美元/盎司', 'yahoo': 'PA=F'},
    # 有色金属 (COMEX/LME期货)
    'HG=F': {'name': '铜', 'unit': '美元/磅', 'yahoo': 'HG=F'},
    'ALI=F': {'name': '铝', 'unit': '美元/吨', 'yahoo': 'ALI=F'},  
    'ZN=F': {'name': '锌', 'unit': '美元/吨', 'yahoo': 'ZN=F'},
}

def get_btc_price():
    """获取比特币价格 (雅虎财经)"""
    try:
        btc = yf.Ticker("BTC-USD")
        info = btc.info
        current = info.get('regularMarketPrice', 0)
        prev = info.get('regularMarketPreviousClose', 0)
        change_pct = ((current - prev) / prev * 100) if prev else 0
        return {
            'name': '比特币',
            'symbol': 'BTC',
            'price': current,
            'change_pct': round(change_pct, 2),
            'unit': '美元'
        }
    except Exception as e:
        # 备用: CoinGecko
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data and 'bitcoin' in data:
                btc = data['bitcoin']
                return {
                    'name': '比特币',
                    'symbol': 'BTC',
                    'price': btc['usd'],
                    'change_pct': round(btc.get('usd_24h_change', 0), 2),
                    'unit': '美元'
                }
        except:
            pass
        return {'name': '比特币', 'symbol': 'BTC', 'error': str(e)[:30]}

def get_metal_from_yahoo(symbol, info):
    """从雅虎财经获取金属价格"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d", interval="1d")
        
        if len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change_pct = ((current - prev) / prev) * 100
            
            return {
                'name': info['name'],
                'symbol': symbol,
                'price': round(current, 2),
                'change_pct': round(change_pct, 2),
                'unit': info['unit']
            }
        elif len(hist) == 1:
            current = hist['Close'].iloc[-1]
            return {
                'name': info['name'],
                'symbol': symbol,
                'price': round(current, 2),
                'change_pct': 0,
                'unit': info['unit']
            }
    except Exception as e:
        pass
    
    # 备用: 新浪财经
    return get_metal_from_sina(symbol, info)

def get_metal_from_sina(symbol, info):
    """新浪财经备用"""
    try:
        sina_map = {
            'GC=F': 'hf_GC',  # 黄金
            'SI=F': 'hf_SI',  # 白银
        }
        if symbol in sina_map:
            url = f"https://hq.sinajs.cn/list={sina_map[symbol]}"
            headers = {'Referer': 'https://finance.sina.com.cn'}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                content = resp.text
                data = content.split('"')[1].split(',')
                if len(data) > 1:
                    price = float(data[0])
                    change = float(data[1])
                    return {
                        'name': info['name'],
                        'symbol': symbol,
                        'price': price,
                        'change_pct': round(change, 2),
                        'unit': info['unit']
                    }
    except:
        pass
    
    return {'name': info['name'], 'symbol': symbol, 'unit': info.get('unit', '美元/盎司'), 'error': '获取失败'}

def get_nickel_price():
    """获取镍价格 (LME镍)"""
    try:
        # 使用LME镍的ETF或相关股票作为参考
        ticker = yf.Ticker("NILA.L")  # LME Nickel ETF
        info = ticker.info
        current = info.get('regularMarketPrice', 0)
        prev = info.get('regularMarketPreviousClose', 0)
        if current and prev:
            change_pct = ((current - prev) / prev) * 100
            return {
                'name': '镍',
                'symbol': 'NIUSD',
                'price': round(current * 100, 2),  # 换算成美元/吨
                'change_pct': round(change_pct, 2),
                'unit': '美元/吨'
            }
    except:
        pass
    
    # 备用: 返回带错误标记的数据
    return {
        'name': '镍',
        'symbol': 'NIUSD',
        'price': 'N/A',
        'change_pct': 0,
        'unit': '美元/吨',
        'error': '暂无数据源'
    }

def generate_report():
    """生成监控报告"""
    beijing = datetime.now(timezone(timedelta(hours=8)))
    utc = datetime.now(timezone.utc)
    
    start_time = datetime.now()
    
    report = f"""
💰 **贵金属 & 加密货币 & 有色金属监控报告**
**检测时间：** {beijing.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)
**UTC时间：** {utc.strftime('%H:%M:%S')}
**数据源：** 雅虎财经 + 新浪财经

---
**🥇 贵金属行情：**

"""
    
    results = []
    
    # 黄金
    data = get_metal_from_yahoo('GC=F', YAHOO_SYMBOLS['GC=F'])
    emoji = "🟢" if data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{data['name']}** (XAUUSD) | {emoji} | **{data.get('price', 'N/A')}** | {data.get('change_pct', 0):+.2f}% | {data['unit']} |\n"
    results.append(data)
    
    # 白银
    data = get_metal_from_yahoo('SI=F', YAHOO_SYMBOLS['SI=F'])
    emoji = "🟢" if data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{data['name']}** (XAGUSD) | {emoji} | **{data.get('price', 'N/A')}** | {data.get('change_pct', 0):+.2f}% | {data['unit']} |\n"
    results.append(data)
    
    # 铂金
    data = get_metal_from_yahoo('PL=F', YAHOO_SYMBOLS['PL=F'])
    emoji = "🟢" if data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{data['name']}** (XPTUSD) | {emoji} | **{data.get('price', 'N/A')}** | {data.get('change_pct', 0):+.2f}% | {data['unit']} |\n"
    results.append(data)
    
    # 钯金
    data = get_metal_from_yahoo('PA=F', YAHOO_SYMBOLS['PA=F'])
    emoji = "🟢" if data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{data['name']}** (XPDUSD) | {emoji} | **{data.get('price', 'N/A')}** | {data.get('change_pct', 0):+.2f}% | {data['unit']} |\n"
    results.append(data)
    
    # 比特币
    report += "\n**₿ 加密货币行情：**\n\n"
    btc_data = get_btc_price()
    emoji = "🟢" if btc_data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{btc_data['name']}** ({btc_data['symbol']}) | {emoji} | **${btc_data.get('price', 'N/A'):,.2f}** | {btc_data.get('change_pct', 0):+.2f}% | {btc_data['unit']} |\n"
    results.append(btc_data)
    
    report += "\n**🔧 有色金属行情：**\n\n"
    
    # 铜
    data = get_metal_from_yahoo('HG=F', YAHOO_SYMBOLS['HG=F'])
    emoji = "🟢" if data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{data['name']}** (HGUSD) | {emoji} | **{data.get('price', 'N/A')}** | {data.get('change_pct', 0):+.2f}% | {data['unit']} |\n"
    results.append(data)
    
    # 铝
    data = get_metal_from_yahoo('ALI=F', YAHOO_SYMBOLS['ALI=F'])
    emoji = "🟢" if data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{data['name']}** (ALIUSD) | {emoji} | **{data.get('price', 'N/A')}** | {data.get('change_pct', 0):+.2f}% | {data['unit']} |\n"
    results.append(data)
    
    # 镍
    data = get_nickel_price()
    emoji = "🟢" if data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{data['name']}** (NIUSD) | {emoji} | **{data.get('price', 'N/A')}** | {data.get('change_pct', 0):+.2f}% | {data['unit']} |\n"
    results.append(data)
    
    # 锌
    data = get_metal_from_yahoo('ZN=F', YAHOO_SYMBOLS['ZN=F'])
    emoji = "🟢" if data.get('change_pct', 0) >= 0 else "🔴"
    report += f"| **{data['name']}** (ZNUSD) | {emoji} | **{data.get('price', 'N/A')}** | {data.get('change_pct', 0):+.2f}% | {data['unit']} |\n"
    results.append(data)
    
    # 异动检测
    big_moves = [r for r in results if abs(r.get('change_pct', 0)) >= 1.5 and 'error' not in r]
    
    report += "\n**⚠️ 异动检测（≥1.5%）：**\n"
    if big_moves:
        for r in big_moves:
            change = r.get('change_pct', 0)
            direction = "上涨" if change > 0 else "下跌"
            report += f"- {r['name']} {direction} **{change:+.2f}%**\n"
    else:
        report += "✅ 市场平稳，无显著异动\n"
    
    # 检测耗时
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    report += f"\n---\n**⏱️ 检测耗时：** {elapsed:.2f}秒\n"
    report += f"**下次报告：** 3分钟后 ({(beijing + timedelta(minutes=3)).strftime('%H:%M:%S')})\n"
    
    return report

def save_report(report):
    """保存报告"""
    log_file = '/Users/cwj18017295567/.openclaw/workspace/metal_monitor.json'
    data = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass
    
    data.append({
        'time': datetime.now(timezone(timedelta(hours=8))).isoformat(),
        'report': report
    })
    data = data[-50:]  # 保留最近50条
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    report = generate_report()
    save_report(report)
    print(report)
