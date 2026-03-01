#!/opt/homebrew/bin/python3.13
"""贵金属监控 + Discord 推送脚本"""
import subprocess
import json
import os

# 运行监控脚本并获取输出
result = subprocess.run(
    ['/opt/homebrew/bin/python3.13', '/Users/cwj18017295567/.openclaw/workspace/metal_monitor.py'],
    capture_output=True,
    text=True
)

report = result.stdout

# 保存到文件
log_file = '/Users/cwj18017295567/.openclaw/workspace/metal_monitor_output.txt'
with open(log_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(report)
print(f"\n报告已保存到: {log_file}")
print("请手动运行以下命令发送到 Discord:")
print(f'openclaw message send --channel discord --target "channel:1476557394665406608" --file "{log_file}"')
