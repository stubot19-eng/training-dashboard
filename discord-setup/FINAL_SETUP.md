# SWARM OS Discord Bots - Complete Setup

## ✅ What You Have Now

- **Webhooks** → Agents can POST to Discord channels ✅
- **Bot code** → Ready to respond to @mentions (just need tokens)

---

## 🚀 Final Step: Create Bot Tokens

### 1. Create Discord Applications (10 min)

Go to https://discord.com/developers/applications

**Create 4 apps:**

**Stu:**
1. New Application → Name: `SWARM-Stu`
2. Bot tab → Add Bot
3. ⚠️ **IMPORTANT**: Enable "MESSAGE CONTENT INTENT"
4. Reset Token → **Copy token**
5. OAuth2 → URL Generator:
   - Scope: `bot`
   - Permissions: Send Messages, Read Messages, Embed Links
   - Copy URL → Open in browser → Invite to SWARM OS

**FitBot:**
- Name: `SWARM-FitBot`
- Same steps

**SourceBot:**
- Name: `SWARM-SourceBot`
- Same steps

**AuditBot:**
- Name: `SWARM-AuditBot`
- Same steps

---

### 2. Set Environment Variables

**Linux/Mac:**
```bash
export STU_TOKEN=your-stu-token-here
export FITBOT_TOKEN=your-fitbot-token-here
export SOURCEBOT_TOKEN=your-sourcebot-token-here
export AUDITBOT_TOKEN=your-auditbot-token-here
```

**Windows:**
```cmd
set STU_TOKEN=your-stu-token-here
set FITBOT_TOKEN=your-fitbot-token-here
set SOURCEBOT_TOKEN=your-sourcebot-token-here
set AUDITBOT_TOKEN=your-auditbot-token-here
```

---

### 3. Install & Run

```bash
cd discord-setup/bots
pip3 install -r requirements.txt
chmod +x run_bots.sh
./run_bots.sh
```

Or run individually:
```bash
STU_TOKEN=xxx python3 stu_bot.py &
FITBOT_TOKEN=xxx python3 fitbot.py &
SOURCEBOT_TOKEN=xxx python3 sourcebot.py &
AUDITBOT_TOKEN=xxx python3 auditbot.py &
```

---

## ✅ Result

Once running, you can:
- `@Stu show missions`
- `@FitBot what's my weight?`
- `@SourceBot check inventory`
- `@AuditBot run security scan`

Plus slash commands: `/missions`, `/stats`, `/inventory`, `/scan`

---

## 🎉 You're Done!

Total time: ~25 minutes
- Webhooks: 15 min ✅
- Bot accounts: 10 min

**SWARM OS Discord command center is fully operational.**
