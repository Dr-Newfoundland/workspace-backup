# MEMORY.md - 长期记忆

_重要的信息、决策和偏好，跨越会话保留。_

---

## 用户偏好

### 沟通风格
- **分段汇报**（强制规则）：
  - 复杂任务必须拆成多步骤
  - 每完成**一个命令/操作** → 立即汇报结果
  - 禁止攒多个结果一起发
  - 等用户看到进度后，再继续下一步
- **流式输出**：偏好整块发送（block streaming ON）
- **主动推进**：不需要每一步都询问，但每条汇报后暂停等待确认

### 任务处理
- 乐于看到分条回复和实时进度
- 不喜欢干等很久后收到大量消息

---

## 重要项目

### 网站项目
- **名称**: Newfoundland 官网
- **链接**: https://dr-newfoundland.github.io/newfoundland-website/
- **仓库**: https://github.com/Dr-Newfoundland/newfoundland-website
- **状态**: ✅ 已上线
- **特点**: 苹果风格丝滑动效

### 工作区备份
- **仓库**: https://github.com/Dr-Newfoundland/workspace-backup
- **创建时间**: 2026-03-01
- **内容**: 完整 OpenClaw 工作区

---

## 配置备忘

- Discord 服务器: 1476555515856293952
- 无需 @mention 即可触发
- GitHub 账号: Dr-Newfoundland

### Cron 定时任务标准模板

**成功案例：** 每3分钟监控报告

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "*/3 * * * *"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "具体任务指令",
    "model": "kimi-coding/kimi-k2-thinking"
  },
  "delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "1476555516535767232"
  }
}
```

**关键参数说明：**
- `sessionTarget`: `isolated` - 独立隔离会话
- `wakeMode`: `now` - 立即唤醒执行
- `payload.kind`: `agentTurn` - 代理自主执行
- `delivery.mode`: `announce` - 完成后播报结果
- `delivery.channel`: `discord` - 发送到Discord
- `delivery.to`: `1476555516535767232` - 目标频道ID

**以后所有定时任务必须参照此模板配置！**

### 每日定时任务安排

| 时间 | 任务 | 说明 |
|------|------|------|
| 09:00 | 每日系统体检 | 检查所有配置，修复问题，分板块汇报 |
| 10:00 | 每日待办检查 | 读取TODO.md，汇报待办清单 |
| 22:00 | 每日待办检查 | 读取TODO.md，汇报待办清单 |

---

## 待办/后续

- [ ] 定期清理临时 JSON 文件
- [ ] 优化监控脚本（A股、美股、金属）
- [ ] 小红书 Cookie 过期提醒

---

_更新: 2026-03-01_
