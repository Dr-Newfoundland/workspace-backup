# OpenClaw 定时任务（Cron）使用指南

## 当前任务状态

**任务名称：** metal-crypto-monitor-v2  
**任务ID：** 1c7ac83a-4f36-4e54-ac0a-97af36e13c3c  
**执行频率：** 每3分钟 (`*/3 * * * *`)  
**状态：** ✅ 已启用

---

## 常用命令

### 查看所有定时任务
```bash
openclaw cron list
```

### 添加新任务
```bash
openclaw cron add \
  --name "任务名称" \
  --cron "*/3 * * * *" \
  --announce \
  --message "要执行的任务内容"
```

### 删除任务
```bash
openclaw cron rm <任务ID>
```

### 查看任务详情
```bash
openclaw cron info <任务ID>
```

---

## Cron 时间格式

```
* * * * *
│ │ │ │ │
│ │ │ │ └── 星期 (0-7, 0和7=周日)
│ │ │ └──── 月份 (1-12)
│ │ └────── 日期 (1-31)
│ └──────── 小时 (0-23)
└────────── 分钟 (0-59)
```

### 常用示例

| 表达式 | 含义 |
|--------|------|
| `*/3 * * * *` | 每3分钟 |
| `0 * * * *` | 每小时整点 |
| `0 9 * * 1-5` | 工作日9:00 |
| `0 0 * * *` | 每天0点 |
| `*/10 9-15 * * 1-5` | 工作日9-15点每10分钟 |

---

## 当前监控脚本

**脚本路径：**
```
/Users/cwj18017295567/.openclaw/workspace/metal_monitor.py
```

**监控内容：**
- 🥇 黄金、白银、铂金、钯金
- ₿ 比特币
- 🔧 铜、铝、镍、锌

**输出日志：**
```
/Users/cwj18017295567/.openclaw/workspace/metal_monitor.json
```

---

## 推送问题解决

如果收不到推送，可能原因：
1. `--announce` 模式依赖子agent输出
2. 子agent可能没有正确路由到当前频道
3. 建议改为直接 `message` 发送

### 替代方案：使用 Heartbeat
编辑 `HEARTBEAT.md`，每30分钟检查一次：
```markdown
每30分钟运行一次贵金属监控脚本，并将结果发送给用户。
```

---

## 手动运行测试

```bash
/opt/homebrew/bin/python3.13 /Users/cwj18017295567/.openclaw/workspace/metal_monitor.py
```

---

文档生成时间：2026-02-27 23:55 UTC
