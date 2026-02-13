# SWARM OS Bot Accounts - Setup Guide

## Step 1: Create Discord Applications (10 min)

Go to https://discord.com/developers/applications

**For EACH agent, do this:**

### Stu
1. Click **New Application** → Name: `SWARM-Stu`
2. Go to **Bot** tab → Click **Add Bot**
3. Under **Privileged Gateway Intents**, enable:
   - ☑️ MESSAGE CONTENT INTENT (required to read @mentions)
4. Click **Reset Token** → **Copy** (save this!)
5. Go to **OAuth2** → **URL Generator**
   - Select scope: `bot`
   - Select permissions:
     - ☑️ Send Messages
     - ☑️ Read Messages/View Channels
     - ☑️ Embed Links
     - ☑️ Use Slash Commands
   - Copy the generated URL at bottom
   - Open that URL in browser → Select SWARM OS server → Authorize

### FitBot
Repeat above with name: `SWARM-FitBot`

### SourceBot
Repeat with name: `SWARM-SourceBot`

### AuditBot
Repeat with name: `SWARM-AuditBot`

---

## Step 2: Save Your Tokens

Create a file called `bot-tokens.env`:

```bash
STU_TOKEN=your-stu-token-here
FITBOT_TOKEN=your-fitbot-token-here
SOURCEBOT_TOKEN=your-sourcebot-token-here
AUDITBOT_TOKEN=your-auditbot-token-here
```

**NEVER share these tokens. Anyone with them can control your bots.**

---

## Step 3: Run the Bots

I'll create Python scripts that run all 4 bots. Each bot:
- Responds when @mentioned
- Can also respond to trigger words ("Stu", "FitBot", etc.)
- Posts to webhooks for system logs

Paste your 4 tokens here when you have them and I'll give you the code.
