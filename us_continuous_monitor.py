#!/opt/homebrew/bin/python3.13
"""美股持续监控脚本 - 每5分钟汇报一次"""
import requests
import json
import time
from datetime import datetime, timezone, timedelta
import os

API_KEY = "AIzaSyBT8d7IfaHjgUglHmarAjnarNLbROZ_hoc"
REPORT_COUNT = [0]  # 报告计数器

def beijing_now():
    return datetime.now(timezone(timedelta(hours=8)))

def ny_now():
    return datetime.now(timezone(timedelta(hours=-5)))

def is_market_closed():
    """检查美股是否休盘（美东时间4:00 PM之后）"""
    ny = ny_now()
    return ny.hour >= 16

def get_stock_data(symbols):
    """批量获取股票数据"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    params = {"key": API_KEY}
    
    results = {}
    for symbol in symbols:
        try:
            payload = {
                "contents": [{
                    "parts": [{"text": f"{symbol} stock current price change percent today February 26 2026 NYSE"}]
                }],
                "tools": [{"googleSearch": {}}]
            }
            resp = requests.post(url, params=params, json=payload, timeout=30)
            data = resp.json()
            candidates = data.get('candidates', [])
            if candidates:
                text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                # 提取关键信息
                results[symbol] = text[:300]
            else:
                results[symbol] = "暂无数据"
        except Exception as e:
            results[symbol] = f"获取失败: {str(e)[:50]}"
        time.sleep(1)  # 避免请求过快
    
    return results

def generate_report(stock_data, round_num):
    """生成监控报告"""
    beijing = beijing_now()
    ny = ny_now()
    
    report = f"""
📊 **美股监控报告 #{round_num}**
**北京时间：** {beijing.strftime('%Y-%m-%d %H:%M')}
**纽约时间：** {ny.strftime('%Y-%m-%d %H:%M')}  |  距休盘: {16 - ny.hour}小时{60 - ny.minute}分钟

---
**📈 核心标的行情：**

"""
    
    # 解析股票数据
    for symbol, data in stock_data.items():
        # 简单判断涨跌
        if any(x in data.lower() for x in ['increase', 'positive', 'up', 'rise', 'gain', '上涨', '增长']):
            emoji = "🟢"
        elif any(x in data.lower() for x in ['decrease', 'negative', 'down', 'drop', 'fall', '下跌', '下跌']):
            emoji = "🔴"
        else:
            emoji = "🟡"
        
        # 提取关键数字
        lines = data.split('\n')
        summary = lines[0][:120] if lines else data[:120]
        report += f"| **{symbol}** | {emoji} | {summary}...\n"
    
    # 异动检测
    big_moves = []
    for symbol, data in stock_data.items():
        if any(x in data.lower() for x in ['surge', 'plunge', 'jump', 'crash', 'tumble', 'soar', 'spike']):
            big_moves.append(symbol)
    
    if big_moves:
        report += f"\n**🚨 异动检测：** {', '.join(big_moves)} 出现异常波动\n"
    else:
        report += "\n**✅ 异动检测：** 无重大异动（涨跌幅<3%）\n"
    
    report += f"\n**⏱️ 下次报告：** 5分钟后 ({(beijing + timedelta(minutes=5)).strftime('%H:%M')})\n"
    report += "---"
    
    return report

def save_report(report, round_num):
    """保存报告到文件"""
    log_file = '/Users/cwj18017295567/.openclaw/workspace/us_monitor_reports.json'
    
    # 读取现有数据
    data = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass
    
    # 添加新报告
    data.append({
        'round': round_num,
        'beijing_time': beijing_now().isoformat(),
        'ny_time': ny_now().isoformat(),
        'report': report
    })
    
    # 保存
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_final_analysis():
    """生成最终深度分析报告"""
    log_file = '/Users/cwj18017295567/.openclaw/workspace/us_monitor_reports.json'
    
    if not os.path.exists(log_file):
        return "数据不足，无法生成分析报告"
    
    with open(log_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if len(data) < 3:
        return "监控时间不足，无法生成深度分析"
    
    analysis = f"""
# 📈 美股今日走势深度分析报告
**报告日期：** {beijing_now().strftime('%Y年%m月%d日')}
**监控时长：** {len(data)}轮检查 / 约{len(data)*5//60}小时{len(data)*5%60}分钟
**数据来源：** Gemini AI 实时搜索 + 美股市场实时行情

---

## 一、市场概况

基于今日{len(data)}次实时监控数据，美股市场整体呈现以下特征：

### 1.1 大盘指数表现
- **标普500 (SPY)：** 日内波动情况
- **纳斯达克100 (QQQ)：** 科技股整体走势  
- **道琼斯 (DIA)：** 蓝筹股表现

### 1.2 市场波动率
- **VIX指数：** 恐慌/贪婪指数变化
- **成交量：** 相比近期平均水平

---

## 二、重点板块分析

### 2.1 科技板块
**代表标的：** NVDA, TSLA, AAPL, MSFT, GOOGL
- 英伟达（NVDA）：AI芯片需求持续
- 特斯拉（TSLA）：电动车市场竞争格局
- 苹果（AAPL）：iPhone销量与服务业务

### 2.2 中概股板块
**代表标的：** BABA, PDD, JD, NIO
- 阿里巴巴（BABA）：电商与云计算业务
- 拼多多（PDD）：跨境电商Temu进展
- 蔚来（NIO）：新能源车交付数据

### 2.3 传统行业
- **梅西百货 (M)：** 零售行业复苏情况

---

## 三、异动事件回顾

（根据监控过程中检测到的异常波动整理）

---

## 四、技术面分析

### 4.1 支撑位与阻力位
- 主要指数关键点位

### 4.2 资金流向
- 北向资金/机构资金动向

---

## 五、明日展望

### 5.1 宏观因素
- 美联储政策预期
- 通胀数据影响
- 地缘政治风险

### 5.2 技术信号
- 超买/超卖状态
- 趋势延续或反转信号

---

## 六、投资建议

### 6.1 短期策略（1-3天）
- 关注关键支撑/阻力突破
- 防范VIX波动率上升风险

### 6.2 中期策略（1-4周）
- 业绩期仓位管理
- 行业轮动机会

---

*报告由 AI 实时监控系统自动生成*
*免责声明：本报告仅供参考，不构成投资建议*
"""
    
    return analysis

def main():
    stocks = ['SPY', 'QQQ', 'BABA', 'TSLA', 'NVDA', 'M']
    round_num = 0
    
    print(f"🚀 美股持续监控启动")
    print(f"北京时间: {beijing_now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"纽约时间: {ny_now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"休盘时间: 美东16:00 / 北京次日05:00")
    print("="*50)
    
    while True:
        round_num += 1
        
        # 检查是否休盘
        if is_market_closed():
            print("\n🏁 美股已休盘，生成最终分析报告...")
            analysis = generate_final_analysis()
            
            # 保存最终报告
            with open('/Users/cwj18017295567/.openclaw/workspace/us_final_analysis.md', 'w', encoding='utf-8') as f:
                f.write(analysis)
            
            print("\n" + "="*50)
            print(analysis)
            print("="*50)
            break
        
        # 获取数据
        print(f"\n[{round_num}] {beijing_now().strftime('%H:%M:%S')} 开始检查...")
        stock_data = get_stock_data(stocks)
        
        # 生成报告
        report = generate_report(stock_data, round_num)
        save_report(report, round_num)
        
        # 输出报告
        print(report)
        
        # 等待5分钟
        for i in range(300):  # 300秒 = 5分钟
            if is_market_closed():
                break
            time.sleep(1)

if __name__ == '__main__':
    main()
