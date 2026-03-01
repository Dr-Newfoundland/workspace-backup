#!/opt/homebrew/bin/python3.13
"""A股实时监控脚本 - 每3分钟汇报"""
import requests
import json
from datetime import datetime, timezone, timedelta
import os

# 监控的A股标的
STOCKS = {
    '000001': '上证指数',
    '000300': '沪深300',
    '000905': '中证500',
    '399006': '创业板指',
    '600519': '贵州茅台',
    '300750': '宁德时代',
    '002594': '比亚迪',
    '601127': '赛力斯',
}

def get_a_stock_data(stock_code, stock_name):
    """获取A股实时数据"""
    try:
        # 使用东方财富API
        if stock_code.startswith('6') or stock_code.startswith('5'):
            # 上海主板
            url = f"https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&volt=2&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f170&secid=1.{stock_code}"
        elif stock_code.startswith('0') or stock_code.startswith('3'):
            # 深圳/创业板
            url = f"https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&volt=2&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f170&secid=0.{stock_code}"
        else:
            # 其他
            url = f"https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&volt=2&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f170&secid=1.{stock_code}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get('data'):
            d = data['data']
            current_price = d.get('f43', 0) / 100 if d.get('f43') else 0
            change_pct = d.get('f170', 0) / 100 if d.get('f170') else 0
            
            return {
                'name': stock_name,
                'code': stock_code,
                'price': current_price,
                'change_pct': change_pct,
            }
    except Exception as e:
        return {'name': stock_name, 'code': stock_code, 'error': str(e)[:30]}
    
    return None

def check_market_status():
    """检查A股是否开市"""
    beijing = datetime.now(timezone(timedelta(hours=8)))
    weekday = beijing.weekday()
    hour = beijing.hour
    minute = beijing.minute
    
    # 周末休市
    if weekday >= 5:
        return False, f"周末休市 ({beijing.strftime('%Y-%m-%d %H:%M')})"
    
    # 交易时间 9:30-11:30, 13:00-15:00
    time_val = hour * 100 + minute
    if (930 <= time_val <= 1130) or (1300 <= time_val <= 1500):
        return True, "交易中"
    else:
        return False, f"非交易时间 ({beijing.strftime('%H:%M')})"

def generate_report():
    """生成监控报告"""
    beijing = datetime.now(timezone(timedelta(hours=8)))
    is_open, status = check_market_status()
    
    report = f"""
📊 **A股监控报告**
**北京时间：** {beijing.strftime('%Y-%m-%d %H:%M:%S')}
**市场状态：** {status}

---
**📈 核心标的行情：**

"""
    
    if not is_open:
        report += "⏸️ 当前非交易时间，展示最新数据：\n\n"
    
    # 获取数据
    results = []
    for code, name in STOCKS.items():
        data = get_a_stock_data(code, name)
        if data and 'error' not in data:
            emoji = "🟢" if data['change_pct'] > 0 else "🔴" if data['change_pct'] < 0 else "⚪"
            results.append({
                'name': name,
                'code': code,
                'price': data['price'],
                'change_pct': data['change_pct'],
                'emoji': emoji
            })
    
    # 排序：涨幅从大到小
    results.sort(key=lambda x: x['change_pct'], reverse=True)
    
    for r in results[:8]:
        report += f"| **{r['name']}** ({r['code']}) | {r['emoji']} | **{r['price']:.2f}** | {r['change_pct']:+.2f}% |\n"
    
    # 检查异动
    big_moves = [r for r in results if abs(r['change_pct']) >= 3]
    if big_moves:
        report += f"\n**🚨 异动检测（≥3%）：**\n"
        for r in big_moves:
            direction = "上涨" if r['change_pct'] > 0 else "下跌"
            report += f"- {r['name']} {direction} **{r['change_pct']:+.2f}%**\n"
    else:
        report += "\n**✅ 异动检测：** 无重大异动（涨跌幅<3%）\n"
    
    report += "\n---\n"
    
    return report, results

def save_report(report):
    """保存报告到文件"""
    log_file = '/Users/cwj18017295567/.openclaw/workspace/a_stock_monitor.json'
    
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
    
    # 只保留最近100条
    data = data[-100:]
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    report, results = generate_report()
    save_report(report)
    print(report)
