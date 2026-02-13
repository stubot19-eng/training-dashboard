# SWARM OS Discord Integration Package
## Complete Setup Guide for Bryce

---

## 🚀 QUICK START (10-Minute Setup)

### Step 1: Create the Server (2 minutes)
1. Open Discord (web or app)
2. Click the **+** icon in your server list
3. Select **"Create My Own"**
4. Choose **"For me and my friends"**
5. Name it: `SWARM OS`
6. Upload `swarm-os-icon.png` as the server icon (included in this package)

### Step 2: Enable Developer Mode (1 minute)
1. Go to **User Settings** (gear icon)
2. Scroll to **Advanced**
3. Toggle **Developer Mode** ON
4. This lets you copy IDs easily

### Step 3: Create Categories & Channels (4 minutes)

Use the channel structure below. Right-click server name → **Create Category** → **Create Channel**

#### Category: 🧠 COMMAND CENTER
| Channel | Type | Purpose |
|---------|------|---------|
| #general | Text | Main chat with Stu (LeadOrchestrator) |
| #missions | Text | Active tasks & mission tracking |

#### Category: 🤖 AGENT ZONES
| Channel | Type | Purpose |
|---------|------|---------|
| #fitness | Text | FitBot activity & health data |
| #sourcing | Text | SourceBot procurement updates |
| #audit | Text | AuditBot logs & compliance checks |

#### Category: ⚙️ SYSTEM
| Channel | Type | Purpose |
|---------|------|---------|
| #logs | Text | System-wide event logs |
| #agent-chat | Text | Inter-agent communication |

### Step 4: Create Roles (2 minutes)

Go to **Server Settings** → **Roles** → **Create Role**

| Role Name | Color | Permissions | Hoisted |
|-----------|-------|-------------|---------|
| @CEO | #FFD700 (Gold) | Administrator | ✅ Yes |
| @LeadOrchestrator | #00D4AA (Teal) | Manage Messages, Manage Webhooks, View Audit Log | ✅ Yes |
| @Agent | #7289DA (Blurple) | Send Messages, Embed Links, Attach Files | ❌ No |

### Step 5: Assign Your Role (30 seconds)
1. Right-click your name in the member list
2. **Roles** → Check **@CEO**
3. Right-click Stu's bot account → **@LeadOrchestrator**

### Step 6: Create Webhooks (1 minute)

Go to each channel → **Settings** (gear icon) → **Integrations** → **Webhooks** → **New Webhook**

Name them exactly:
- `Stu-Orchestrator` (for #general)
- `FitBot-Agent` (for #fitness)
- `SourceBot-Agent` (for #sourcing)
- `AuditBot-Agent` (for #audit)
- `SWARM-System` (for #logs)

**Copy each webhook URL** and save it - you'll need to give these to your agents.

---

## 📋 COMPLETE REFERENCE

### Server Structure Diagram

```
SWARM OS
├── 🧠 COMMAND CENTER
│   ├── #general (Stu's main interface)
│   └── #missions (active task tracking)
│
├── 🤖 AGENT ZONES
│   ├── #fitness (FitBot)
│   ├── #sourcing (SourceBot)
│   └── #audit (AuditBot)
│
└── ⚙️ SYSTEM
    ├── #logs (system events)
    └── #agent-chat (bot-to-bot)
```

### Permission Matrix

| Channel | @CEO | @LeadOrchestrator | @Agent | @everyone |
|---------|------|-------------------|--------|-----------|
| #general | ✅ All | ✅ All | ✅ Send/Read | ❌ None |
| #missions | ✅ All | ✅ All | ✅ Send/Read | ❌ None |
| #fitness | ✅ All | ✅ All | ✅ Send/Read | ❌ None |
| #sourcing | ✅ All | ✅ All | ✅ Send/Read | ❌ None |
| #audit | ✅ All | ✅ All | ✅ Send/Read | ❌ None |
| #logs | ✅ All | ✅ All | ✅ Send Only | ❌ None |
| #agent-chat | ✅ All | ✅ All | ✅ All | ❌ None |

---

## 🔗 WEBHOOK URL PLACEHOLDER FILE

**IMPORTANT:** Replace these placeholders with your actual webhook URLs after creating them.

Create a file named `discord-webhooks.env`:

```bash
# SWARM OS Discord Webhooks
# Created: $(date)
# Server: SWARM OS

# Command Center
WEBHOOK_GENERAL=https://discord.com/api/webhooks/YOUR_GENERAL_WEBHOOK_ID/YOUR_GENERAL_WEBHOOK_TOKEN
WEBHOOK_MISSIONS=https://discord.com/api/webhooks/YOUR_MISSIONS_WEBHOOK_ID/YOUR_MISSIONS_WEBHOOK_TOKEN

# Agent Zones
WEBHOOK_FITNESS=https://discord.com/api/webhooks/YOUR_FITNESS_WEBHOOK_ID/YOUR_FITNESS_WEBHOOK_TOKEN
WEBHOOK_SOURCING=https://discord.com/api/webhooks/YOUR_SOURCING_WEBHOOK_ID/YOUR_SOURCING_WEBHOOK_TOKEN
WEBHOOK_AUDIT=https://discord.com/api/webhooks/YOUR_AUDIT_WEBHOOK_ID/YOUR_AUDIT_WEBHOOK_TOKEN

# System
WEBHOOK_LOGS=https://discord.com/api/webhooks/YOUR_LOGS_WEBHOOK_ID/YOUR_LOGS_WEBHOOK_TOKEN
WEBHOOK_AGENT_CHAT=https://discord.com/api/webhooks/YOUR_AGENT_CHAT_WEBHOOK_ID/YOUR_AGENT_CHAT_WEBHOOK_TOKEN
```

---

## 🤖 AGENT CONFIGURATION

Each agent should use their respective webhook to post updates. Here's the configuration format:

### Stu (LeadOrchestrator)
```json
{
  "agent_name": "Stu",
  "role": "LeadOrchestrator",
  "webhook_url": "${WEBHOOK_GENERAL}",
  "primary_channel": "#general",
  "secondary_channels": ["#missions", "#logs"],
  "avatar_url": "https://i.imgur.com/swarm-stu.png"
}
```

### FitBot
```json
{
  "agent_name": "FitBot",
  "role": "Agent",
  "webhook_url": "${WEBHOOK_FITNESS}",
  "primary_channel": "#fitness",
  "secondary_channels": ["#agent-chat"],
  "avatar_url": "https://i.imgur.com/swarm-fitbot.png"
}
```

### SourceBot
```json
{
  "agent_name": "SourceBot",
  "role": "Agent",
  "webhook_url": "${WEBHOOK_SOURCING}",
  "primary_channel": "#sourcing",
  "secondary_channels": ["#agent-chat"],
  "avatar_url": "https://i.imgur.com/swarm-sourcebot.png"
}
```

### AuditBot
```json
{
  "agent_name": "AuditBot",
  "role": "Agent",
  "webhook_url": "${WEBHOOK_AUDIT}",
  "primary_channel": "#audit",
  "secondary_channels": ["#logs", "#agent-chat"],
  "avatar_url": "https://i.imgur.com/swarm-auditbot.png"
}
```

---

## 📱 WELCOME MESSAGES

See `welcome-messages.md` for ready-to-post welcome templates.

---

## 🎨 VISUAL ASSETS

See `visual-assets.md` for:
- Server icon specifications
- Avatar image requirements
- Color scheme reference
- Embed styling guidelines

---

## ✅ POST-SETUP CHECKLIST

- [ ] Server created with name "SWARM OS"
- [ ] Server icon uploaded
- [ ] 6 channels created across 3 categories
- [ ] 3 roles created with correct permissions
- [ ] Your account assigned @CEO role
- [ ] 6 webhooks created and URLs copied
- [ ] `discord-webhooks.env` file created with real URLs
- [ ] Welcome messages posted in #general
- [ ] Agent configuration files updated with webhook URLs

---

## 🆘 TROUBLESHOOTING

**Webhook messages not appearing?**
- Check webhook URL is correct
- Ensure webhook has permission to post in that channel
- Verify channel isn't on slowmode

**Agents can't post?**
- Check @Agent role has "Send Messages" permission
- Verify channel-specific permissions aren't overriding role permissions

**Can't create webhooks?**
- You need "Manage Webhooks" permission
- Check your role hierarchy

---

**Package Version:** 1.0  
**Created for:** Bryce's SWARM OS  
**Setup Time:** ~10 minutes
