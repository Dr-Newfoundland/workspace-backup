#!/opt/homebrew/bin/python3.13
"""贵金属监控 + Discord 推送脚本"""
import subprocess
import json
import os
import time

# 运行监控脚本
result = subprocess.run(
    ['/opt/homebrew/bin/python3.13', '/Users/cwj18017295567/.openclaw/workspace/metal_monitor.py'],
    capture_output=True,
    text=True
)

report = result.stdout

# 保存报告到临时文件
temp_file = '/tmp/metal_report.txt'
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(report)

# 使用 openclaw message 发送
subprocess.run([
    'openclaw', 'message', 'send',
    '--channel', 'discord',
    '--target', 'channel:1476557394665406608',
    '--content', report[:1900]  # Discord 限制2000字符
], capture_output=True)

print(report)
print("\n✅ 报告已发送到 Discord")
