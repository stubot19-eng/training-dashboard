# SWARM OS Discord Server - Quick Reference Card

## 🎯 At a Glance

```
Server: SWARM OS
Owner: Bryce (@CEO)
Channels: 6 | Roles: 3 | Webhooks: 6
Theme: Futuristic Agent Ecosystem
```

---

## 📁 Channel Quick List

| Category | Channel | Agent | Purpose |
|----------|---------|-------|---------|
| 🧠 COMMAND | #general | Stu | Main command interface |
| 🧠 COMMAND | #missions | Stu | Active task tracking |
| 🤖 AGENTS | #fitness | FitBot | Health/performance |
| 🤖 AGENTS | #sourcing | SourceBot | Procurement |
| 🤖 AGENTS | #audit | AuditBot | Security/compliance |
| ⚙️ SYSTEM | #logs | All | System events |
| ⚙️ SYSTEM | #agent-chat | All | Bot coordination |

---

## 👥 Role Hierarchy

```
@CEO (Gold)
  └── Administrator - Full control
      
@LeadOrchestrator (Teal)  
  └── Manage Messages, Webhooks, Audit Log
      
@Agent (Blurple)
  └── Send Messages, Embed Links, Attach Files
```

---

## 🔗 Webhook Mapping

| Webhook Name | Channel | Used By |
|--------------|---------|---------|
| Stu-Orchestrator | #general | Stu |
| Stu-Missions | #missions | Stu |
| FitBot-Agent | #fitness | FitBot |
| SourceBot-Agent | #sourcing | SourceBot |
| AuditBot-Agent | #audit | AuditBot |
| SWARM-System | #logs | All agents |
| Agent-Chat | #agent-chat | All agents |

---

## 📝 Quick Commands

### Creating a Mission
```
Stu, create mission: [name]
Priority: [High/Medium/Low]
Objective: [description]
Assign to: [Agent]
```

### Agent Call
```
@[AgentName], [command]
```

Examples:
- `@FitBot, show weekly stats`
- `@SourceBot, find best price on protein powder`
- `@AuditBot, run security scan`

---

## 🚨 Alert Levels

| Emoji | Level | Response Time | Example |
|-------|-------|---------------|---------|
| 🟢 | Normal | Routine | Daily status |
| 🟡 | Advisory | Same day | Minor issue |
| 🟠 | Warning | Within hours | Performance concern |
| 🔴 | Critical | Immediate | Security breach |

---

## 🔐 Security Notes

- Webhook URLs = SECRET KEYS
- Never post webhook URLs in chat
- AuditBot monitors #logs for anomalies
- @Agent role intentionally limited

---

## 📞 Support

If something breaks:
1. Check #logs for errors
2. Verify webhook permissions
3. Confirm agent role assignments
4. Ping @LeadOrchestrator (Stu)

---

*Print this and keep it handy!*
