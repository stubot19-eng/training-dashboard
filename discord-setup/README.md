# SWARM OS - Complete Setup Package

## 🎯 For Bryce (2 Minutes)

### Step 1: Create Server (30 sec)
```
Discord → + → Create My Own → For me and my friends
Name: SWARM OS
```

### Step 2: Invite Setup Bot (90 sec)
1. Click: https://discord.com/oauth2/authorize?client_id=SETUP_BOT_ID&permissions=8&scope=bot
2. Select "SWARM OS" server
3. Authorize

✅ The bot auto-creates everything else.

---

## 🤖 For Agents (30 Minutes)

### Phase 1: Setup (10 min)

**1. Install dependencies:**
```bash
pip3 install discord.py aiohttp
```

**2. Run the setup bot:**
```bash
python3 swarm_discord_setup.py \
  --server "SWARM OS" \
  --token "SETUP_BOT_TOKEN"
```

This creates:
- 3 categories (Command Center, Agent Zones, System)
- 7 channels (#general, #missions, #fitness, #sourcing, #audit, #logs, #agent-chat)
- 3 roles (@CEO, @LeadOrchestrator, @Agent)
- 7 webhooks (one per channel)
- Welcome messages posted

**Output:** `discord_webhooks.json` and `discord_webhooks.env`

### Phase 2: Deploy Agents (20 min)

**1. Run deployment script:**
```bash
chmod +x deploy_agents.sh
./deploy_agents.sh
```

This creates 4 agent bot files in `agents/` folder.

**2. Get Discord bot tokens:**
- Visit: https://discord.com/developers/applications
- Create 4 applications
- Add Bot → Copy Token for each

**3. Set tokens and run:**
```bash
cd agents

export AGENT_DISCORD_TOKEN="stu-token"
python3 Stu.py &

export AGENT_DISCORD_TOKEN="fitbot-token"
python3 FitBot.py &

export AGENT_DISCORD_TOKEN="sourcebot-token"
python3 SourceBot.py &

export AGENT_DISCORD_TOKEN="auditbot-token"
python3 AuditBot.py &
```

**4. Invite agent bots:**
Generate invite links for each:
```
https://discord.com/oauth2/authorize?client_id=BOT_CLIENT_ID&permissions=3136&scope=bot
```
(permissions = Send Messages + Read Messages + Embed Links)

---

## 📁 Files Included

| File | Purpose |
|------|---------|
| `swarm_discord_setup.py` | Auto-creates server structure |
| `agent_bot_template.py` | Template for each agent |
| `deploy_agents.sh` | Deploys all 4 agents |
| `SWARM_DISCORD_SETUP.md` | Full setup guide |
| `welcome-messages.md` | Welcome message templates |
| `visual-assets.md` | Branding guide |
| `discord-webhooks.env.template` | Webhook URL template |
| `quick-reference.md` | Command cheat sheet |

---

## 🔗 Bot Invite Links

**Setup Bot (Admin - for initial setup):**
```
https://discord.com/oauth2/authorize?client_id=SETUP_CLIENT_ID&permissions=8&scope=bot
```

**Agent Bots (Limited permissions):**
```
Stu: https://discord.com/oauth2/authorize?client_id=STU_CLIENT_ID&permissions=3136&scope=bot
FitBot: https://discord.com/oauth2/authorize?client_id=FITBOT_CLIENT_ID&permissions=3136&scope=bot
SourceBot: https://discord.com/oauth2/authorize?client_id=SOURCEBOT_CLIENT_ID&permissions=3136&scope=bot
AuditBot: https://discord.com/oauth2/authorize?client_id=AUDITBOT_CLIENT_ID&permissions=3136&scope=bot
```

---

## ✅ Result

Bryce gets:
- 7 organized channels
- 3 role levels
- 7 webhooks
- 4 interactive agents responding to @mentions
- Welcome messages posted
- Full command center operational

**Time invested:**
- Bryce: 2 minutes
- Agents: 30 minutes
- Total: 32 minutes to full SWARM OS Discord command center
