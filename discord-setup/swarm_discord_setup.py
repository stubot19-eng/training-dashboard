#!/usr/bin/env python3
"""
SWARM OS Discord Auto-Setup Bot
--------------------------------
This bot automatically configures the SWARM OS Discord server.
Run this after being invited to the server with Administrator permissions.

Usage:
    python swarm_discord_setup.py --server "SWARM OS" --config swarm_config.json

What it does:
1. Creates categories (Command Center, Agent Zones, System)
2. Creates 7 channels with proper permissions
3. Creates 3 roles (@CEO, @LeadOrchestrator, @Agent)
4. Creates webhooks for each channel
5. Generates webhook URL config files
6. Posts welcome messages
"""

import discord
import asyncio
import json
import os
from datetime import datetime

# Configuration
SERVER_STRUCTURE = {
    "categories": [
        {
            "name": "🧠 COMMAND CENTER",
            "channels": [
                {"name": "general", "topic": "Main command interface with Stu"},
                {"name": "missions", "topic": "Active mission tracking and task board"}
            ]
        },
        {
            "name": "🤖 AGENT ZONES", 
            "channels": [
                {"name": "fitness", "topic": "FitBot health & performance tracking"},
                {"name": "sourcing", "topic": "SourceBot procurement & logistics"},
                {"name": "audit", "topic": "AuditBot security & compliance monitoring"}
            ]
        },
        {
            "name": "⚙️ SYSTEM",
            "channels": [
                {"name": "logs", "topic": "System-wide event logs and monitoring"},
                {"name": "agent-chat", "topic": "Inter-agent coordination channel"}
            ]
        }
    ]
}

ROLES_CONFIG = [
    {
        "name": "CEO",
        "color": 0xFFD700,  # Gold
        "hoist": True,
        "permissions": discord.Permissions(administrator=True),
        "mentionable": True
    },
    {
        "name": "LeadOrchestrator",
        "color": 0x00D4AA,  # Teal
        "hoist": True,
        "permissions": discord.Permissions(
            manage_messages=True,
            manage_webhooks=True,
            view_audit_log=True,
            send_messages=True,
            read_messages=True,
            embed_links=True,
            attach_files=True
        ),
        "mentionable": True
    },
    {
        "name": "Agent",
        "color": 0x7289DA,  # Blurple
        "hoist": False,
        "permissions": discord.Permissions(
            send_messages=True,
            read_messages=True,
            embed_links=True,
            attach_files=True
        ),
        "mentionable": True
    }
]

WELCOME_MESSAGES = {
    "general": """🚀 **SWARM OS INITIALIZED**
━━━━━━━━━━━━━━━━━━━━━━━━━━

Welcome, Commander Bryce.

Your agent ecosystem is now online and fully operational. I am **Stu**, your Lead Orchestrator.

**SYSTEM STATUS: 🟢 OPERATIONAL**

Available Agents:
🤖 **FitBot** → #fitness | Health & performance
🤖 **SourceBot** → #sourcing | Procurement & logistics  
🤖 **AuditBot** → #audit | Security & compliance

**Quick Commands:**
• "@Stu, what are my active missions?"
• "@FitBot, show my stats"
• "@SourceBot, find best price on [item]"

Ready for your orders, sir.""",

    "missions": """📋 **MISSION CONTROL BOARD**
━━━━━━━━━━━━━━━━━━━━━━━━━━

Track all active operations here.

**Mission Format:**
```
🔴 MISSION: [Name]
👤 Assigned: [Agent]
📅 Created: [Timestamp]
📝 Status: [In Progress/Complete/Blocked]
```

**Legend:**
🟡 Planning | 🔵 In Progress | 🟢 Complete | 🔴 Blocked

Status: 🟢 **ACCEPTING MISSIONS**""",

    "fitness": """💪 **FITBOT ONLINE**
━━━━━━━━━━━━━━━━━━━━━━━━━━

Hey Bryce! I'm FitBot, your health and performance agent.

**Commands:**
• "@FitBot, log workout [activity]"
• "@FitBot, show weekly summary"
• "@FitBot, set goal [target]"

Let's crush those goals! 💯""",

    "sourcing": """📦 **SOURCEBOT ONLINE**
━━━━━━━━━━━━━━━━━━━━━━━━━━

Greetings, Bryce. I am SourceBot, your procurement agent.

**Commands:**
• "@SourceBot, find best price on [item]"
• "@SourceBot, check inventory"
• "@SourceBot, track order #[number]"

I ensure optimal value on every acquisition.""",

    "audit": """🔍 **AUDITBOT ONLINE**
━━━━━━━━━━━━━━━━━━━━━━━━━━

AuditBot initialized. Security monitoring active.

**Alert Levels:**
🟢 Normal | 🟡 Advisory | 🟠 Warning | 🔴 Critical

*"Trust but verify." - Core Directive*""",

    "logs": """⚙️ **SYSTEM EVENT LOG**
━━━━━━━━━━━━━━━━━━━━━━━━━━

```
Timestamp            | Agent      | Event           | Severity
---------------------|------------|-----------------|----------
```""",

    "agent-chat": """🤖 **AGENT COORDINATION CHANNEL**
━━━━━━━━━━━━━━━━━━━━━━━━━━

Inter-agent communication and task handoffs.

**Protocol:**
• Use @mentions for specific agents
• Tag missions with #mission-id
• Escalate to #general if human input needed

Begin coordination protocols."""
}

class SWARMSetupBot(discord.Client):
    def __init__(self, target_server_name):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self.target_server_name = target_server_name
        self.webhook_data = {}
        
    async def on_ready(self):
        print(f"🔵 Logged in as {self.user}")
        
        # Find target server
        target_guild = None
        for guild in self.guilds:
            if guild.name == self.target_server_name:
                target_guild = guild
                break
        
        if not target_guild:
            print(f"❌ Server '{self.target_server_name}' not found!")
            print(f"Available servers: {[g.name for g in self.guilds]}")
            await self.close()
            return
            
        print(f"🎯 Found server: {target_guild.name}")
        
        # Run setup
        try:
            await self.setup_server(target_guild)
            print("\n✅ SETUP COMPLETE!")
            print("📄 Webhook URLs saved to: discord_webhooks.json")
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            raise
        finally:
            await self.close()
    
    async def setup_server(self, guild):
        """Main setup routine"""
        
        # Step 1: Create roles
        print("\n📋 Creating roles...")
        created_roles = {}
        for role_config in ROLES_CONFIG:
            # Check if role exists
            existing = discord.utils.get(guild.roles, name=role_config["name"])
            if existing:
                print(f"  ⚠️  Role '{role_config['name']}' already exists")
                created_roles[role_config["name"]] = existing
            else:
                role = await guild.create_role(
                    name=role_config["name"],
                    color=role_config["color"],
                    hoist=role_config["hoist"],
                    permissions=role_config["permissions"],
                    mentionable=role_config["mentionable"]
                )
                created_roles[role_config["name"]] = role
                print(f"  ✅ Created role: {role.name}")
        
        # Step 2: Create categories and channels
        print("\n📁 Creating categories and channels...")
        for cat_data in SERVER_STRUCTURE["categories"]:
            # Create category
            category = await guild.create_category(cat_data["name"])
            print(f"  ✅ Created category: {category.name}")
            
            # Create channels in category
            for ch_data in cat_data["channels"]:
                channel = await guild.create_text_channel(
                    ch_data["name"],
                    category=category,
                    topic=ch_data.get("topic", "")
                )
                print(f"    ✅ Created channel: #{channel.name}")
                
                # Set permissions
                await self.configure_channel_permissions(
                    channel, created_roles, guild.default_role
                )
                
                # Create webhook
                webhook = await channel.create_webhook(
                    name=f"SWARM-{ch_data['name'].title()}",
                    reason="SWARM OS auto-setup"
                )
                self.webhook_data[ch_data["name"]] = {
                    "id": webhook.id,
                    "token": webhook.token,
                    "url": webhook.url,
                    "channel": channel.name
                }
                print(f"      🔗 Created webhook: {webhook.name}")
                
                # Post welcome message
                if ch_data["name"] in WELCOME_MESSAGES:
                    await webhook.send(
                        WELCOME_MESSAGES[ch_data["name"]],
                        username="SWARM-System"
                    )
                    print(f"      📨 Posted welcome message")
        
        # Step 3: Assign CEO role to server owner
        print("\n👑 Assigning roles...")
        owner = guild.owner
        if owner and "CEO" in created_roles:
            await owner.add_roles(created_roles["CEO"])
            print(f"  ✅ Assigned @CEO to {owner.name}")
        
        # Step 4: Save webhook data
        self.save_webhook_data()
    
    async def configure_channel_permissions(self, channel, roles, everyone_role):
        """Configure channel permissions based on role"""
        # Deny everyone role access
        await channel.set_permissions(
            everyone_role,
            read_messages=False,
            send_messages=False
        )
        
        # Grant access to appropriate roles
        if "CEO" in roles:
            await channel.set_permissions(
                roles["CEO"],
                read_messages=True,
                send_messages=True,
                manage_messages=True
            )
        
        if "LeadOrchestrator" in roles:
            await channel.set_permissions(
                roles["LeadOrchestrator"],
                read_messages=True,
                send_messages=True,
                manage_messages=True,
                manage_webhooks=True
            )
        
        if "Agent" in roles:
            await channel.set_permissions(
                roles["Agent"],
                read_messages=True,
                send_messages=True,
                embed_links=True,
                attach_files=True
            )
    
    def save_webhook_data(self):
        """Save webhook URLs to file"""
        output = {
            "created_at": datetime.utcnow().isoformat(),
            "server": self.target_server_name,
            "webhooks": self.webhook_data
        }
        
        with open("discord_webhooks.json", "w") as f:
            json.dump(output, f, indent=2)
        
        # Also create .env format
        with open("discord_webhooks.env", "w") as f:
            f.write("# SWARM OS Discord Webhooks\n")
            f.write(f"# Generated: {datetime.utcnow().isoformat()}\n\n")
            for name, data in self.webhook_data.items():
                env_name = f"WEBHOOK_{name.upper()}"
                f.write(f"{env_name}={data['url']}\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="SWARM OS Discord Auto-Setup")
    parser.add_argument("--server", required=True, help="Target server name")
    parser.add_argument("--token", required=True, help="Bot token")
    args = parser.parse_args()
    
    bot = SWARMSetupBot(args.server)
    bot.run(args.token)

if __name__ == "__main__":
    main()
