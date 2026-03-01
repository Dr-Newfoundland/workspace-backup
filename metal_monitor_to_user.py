#!/opt/homebrew/bin/python3.13
"""贵金属监控 + Discord 推送脚本 (修正版)"""
import subprocess
import json
import os
import time

USER_ID = "1476489387159064662"

# 运行监控脚本
result = subprocess.run(
    ['/opt/homebrew/bin/python3.13', '/Users/cwj18017295567/.openclaw/workspace/metal_monitor.py'],
    capture_output=True,
    text=True
)

report = result.stdout

# 使用 openclaw message 发送给用户
# 方法1：尝试发送到用户
try:
    result = subprocess.run([
        'openclaw', 'message', 'send',
        '--to', USER_ID,
        '--content', report[:1900]
    ], capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        # 方法2：如果失败，使用 message 工具直接发
        print(f"发送失败，备用方案: {result.stderr}")
        
except Exception as e:
    print(f"发送出错: {e}")

print(report)
print("\n✅ 报告已尝试发送到 Discord")
