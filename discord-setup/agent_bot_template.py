#!/usr/bin/env python3
"""
SWARM Agent Bot Template
------------------------
Base template for each agent to connect to Discord and respond to mentions.

Each agent should:
1. Copy this file
2. Customize the agent_config section
3. Run: python agent_bot.py

Required: pip install discord.py
"""

import discord
import asyncio
import os
import json
from datetime import datetime
from discord.ext import commands

# ==================== AGENT CONFIGURATION ====================
# Customize this section for each agent

AGENT_CONFIG = {
    "name": "Stu",  # Change for each agent: FitBot, SourceBot, AuditBot
    "role": "LeadOrchestrator",  # CEO, LeadOrchestrator, Agent
    "discord_token": os.getenv("AGENT_DISCORD_TOKEN"),  # Set this env var
    
    # Webhook for posting updates (optional)
    "webhook_url": os.getenv("WEBHOOK_GENERAL"),
    
    # Channels this agent monitors
    "channels": ["general", "missions", "logs"],
    
    # Color for embeds
    "color": 0x00D4AA,  # Stu=Teal, FitBot=Green, SourceBot=Blue, AuditBot=Red
    
    # Avatar URL (optional)
    "avatar_url": None,
    
    # Response triggers (in addition to @mentions)
    "triggers": ["stu", "orchestrator"]
}

# Command handlers - customize for each agent's capabilities
class AgentCommands:
    """Define agent-specific commands here"""
    
    @staticmethod
    async def status(agent, ctx):
        """Default status command"""
        embed = discord.Embed(
            title=f"🤖 {agent.config['name']} Status",
            description="All systems operational.",
            color=agent.config['color'],
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Role", value=agent.config['role'], inline=True)
        embed.add_field(name="Uptime", value=agent.get_uptime(), inline=True)
        embed.add_field(name="Channels", value=", ".join(f"#{c}" for c in agent.config['channels']), inline=False)
        await ctx.send(embed=embed)
    
    @staticmethod
    async def help_command(agent, ctx):
        """Help command - customize per agent"""
        embed = discord.Embed(
            title=f"{agent.config['name']} Commands",
            description="Available commands (use with @mention):",
            color=agent.config['color']
        )
        embed.add_field(
            name="General",
            value="`status` - Check system status\n`help` - Show this message",
            inline=False
        )
        await ctx.send(embed=embed)

# ==================== BOT IMPLEMENTATION ====================

class SWARMAgentBot(commands.Bot):
    def __init__(self, config):
        self.config = config
        self.start_time = datetime.utcnow()
        
        intents = discord.Intents.default()
        intents.message_content = True  # Required to read message content
        intents.members = True
        
        super().__init__(
            command_prefix="!",  # Fallback prefix
            intents=intents,
            help_command=None  # We'll use custom help
        )
        
        self.commands_map = {
            "status": AgentCommands.status,
            "help": AgentCommands.help_command,
            # Add agent-specific commands here
        }
    
    def get_uptime(self):
        delta = datetime.utcnow() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"
    
    async def on_ready(self):
        print(f"🟢 {self.config['name']} is online!")
        print(f"   Discord ID: {self.user.id}")
        print(f"   Connected to {len(self.guilds)} server(s)")
        
        # Set status
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name="for @mentions"
        )
        await self.change_presence(activity=activity)
    
    async def on_message(self, message):
        # Ignore own messages
        if message.author == self.user:
            return
        
        # Check if bot is mentioned
        if self.user in message.mentions:
            await self.handle_mention(message)
            return
        
        # Check for trigger words
        content_lower = message.content.lower()
        for trigger in self.config.get('triggers', []):
            if trigger in content_lower:
                await self.handle_mention(message)
                return
    
    async def handle_mention(self, message):
        """Handle @mention or trigger word"""
        # Extract command from message
        content = message.content
        
        # Remove mention from content
        for mention in message.mentions:
            content = content.replace(f"<@{mention.id}>", "")
            content = content.replace(f"<@!{mention.id}>", "")
        
        content = content.strip().lower()
        
        # Parse command
        parts = content.split()
        if not parts:
            await message.channel.send(f"👋 Hello! I'm {self.config['name']}. Use `@{self.config['name']} help` for commands.")
            return
        
        command = parts[0]
        args = parts[1:]
        
        # Execute command
        if command in self.commands_map:
            try:
                await self.commands_map[command](self, message)
            except Exception as e:
                await message.channel.send(f"❌ Error executing command: {e}")
        else:
            await self.handle_unknown_command(message, command)
    
    async def handle_unknown_command(self, message, command):
        """Handle unknown commands - override for custom behavior"""
        await message.channel.send(
            f"Unknown command: `{command}`. Try `@{self.config['name']} help` for available commands."
        )
    
    async def post_to_webhook(self, content, embed=None):
        """Post update via webhook if configured"""
        import aiohttp
        
        webhook_url = self.config.get('webhook_url')
        if not webhook_url:
            return
        
        payload = {
            "content": content,
            "username": self.config['name']
        }
        if embed:
            payload["embeds"] = [embed.to_dict()]
        if self.config.get('avatar_url'):
            payload["avatar_url"] = self.config['avatar_url']
        
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as resp:
                return resp.status == 204

def main():
    bot = SWARMAgentBot(AGENT_CONFIG)
    
    if not AGENT_CONFIG['discord_token']:
        print("❌ Error: AGENT_DISCORD_TOKEN environment variable not set!")
        print("   Set it with: export AGENT_DISCORD_TOKEN='your-bot-token'")
        return
    
    bot.run(AGENT_CONFIG['discord_token'])

if __name__ == "__main__":
    main()
