#!/usr/bin/env python3
"""
SWARM OS - Stu Bot
LeadOrchestrator - Responds to @mentions and commands
"""

import discord
import asyncio
import os
import aiohttp
from discord.ext import commands
from datetime import datetime

# Bot configuration
TOKEN = os.getenv('STU_TOKEN')
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1471913803968024841/MXfEOeJcTzxU5ltMHntGb_mQ0hBE2urFaGvrj7GfMvyltyjIKUHua9H2mTNWy0TC--9Z'

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Active missions storage
active_missions = []

@bot.event
async def on_ready():
    print(f'🟢 Stu is online! Logged in as {bot.user}')
    print(f'   Connected to {len(bot.guilds)} server(s)')
    
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name='@mentions'),
        status=discord.Status.online
    )
    
    # Send startup message
    await post_webhook('🚀 **Stu ONLINE**\nStatus: 🟢 Operational\nReady for commands.')

@bot.event
async def on_message(message):
    # Ignore own messages
    if message.author == bot.user:
        return
    
    # Check if mentioned
    if bot.user in message.mentions:
        await handle_mention(message)
        return
    
    # Check for trigger words
    content_lower = message.content.lower()
    if any(trigger in content_lower for trigger in ['stu', 'orchestrator', 'lead']):
        if not message.content.startswith('!'):
            await handle_mention(message)
            return
    
    await bot.process_commands(message)

async def handle_mention(message):
    """Handle @mention or trigger word"""
    content = message.content
    
    # Remove mentions from content
    for mention in message.mentions:
        content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
    content = content.strip()
    
    print(f'[Stu] Received: {content}')
    
    # Parse natural language commands
    content_lower = content.lower()
    
    if any(word in content_lower for word in ['mission', 'missions', 'task', 'tasks']):
        await show_missions(message.channel)
    
    elif any(word in content_lower for word in ['agent', 'agents', 'bot', 'bots', 'status']):
        await show_agents(message.channel)
    
    elif any(word in content_lower for word in ['help', 'command', 'commands']):
        await show_help(message.channel)
    
    elif any(word in content_lower for word in ['hello', 'hi', 'hey']):
        await message.channel.send(f'👋 Hello Bryce! Stu here. What can I do for you?')
    
    elif 'dashboard' in content_lower:
        await message.channel.send('📊 Dashboard live at: https://training-dashboard-gamma.vercel.app/swarm-os.html')
    
    else:
        await message.channel.send(f'📝 I heard you say: "{content}"\n\nTry asking me about:\n• Missions\n• Agent status\n• Help/commands')

async def show_missions(channel):
    """Show active missions"""
    embed = discord.Embed(
        title='📋 Active Missions',
        description='Current SWARM operations',
        color=0x00D4AA,
        timestamp=datetime.utcnow()
    )
    
    if active_missions:
        for mission in active_missions:
            embed.add_field(
                name=f"🔵 {mission['name']}",
                value=f"Agent: {mission['agent']}\nStatus: {mission['status']}",
                inline=False
            )
    else:
        embed.add_field(
            name='No Active Missions',
            value='Use "Create mission: [name]" to start one',
            inline=False
        )
    
    await channel.send(embed=embed)

async def show_agents(channel):
    """Show agent status"""
    embed = discord.Embed(
        title='🤖 Agent Fleet Status',
        description='All SWARM agents',
        color=0x00D4AA,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name='Stu', value='🟢 Online | LeadOrchestrator', inline=False)
    embed.add_field(name='FitBot', value='🟢 Online | #fitness', inline=True)
    embed.add_field(name='SourceBot', value='🟢 Online | #sourcing', inline=True)
    embed.add_field(name='AuditBot', value='🟢 Online | #audit', inline=True)
    
    await channel.send(embed=embed)

async def show_help(channel):
    """Show help"""
    embed = discord.Embed(
        title='📖 Stu Commands',
        description='I respond to @mentions or trigger words',
        color=0x00D4AA
    )
    
    embed.add_field(
        name='Natural Language',
        value='@Stu show missions\n@Stu agent status\n@Stu dashboard\n@Stu help',
        inline=False
    )
    
    embed.add_field(
        name='Slash Commands',
        value='/missions - Show active missions\n/agents - Show agent status\n/help - Show this message',
        inline=False
    )
    
    await channel.send(embed=embed)

async def post_webhook(content, embed=None):
    """Post to webhook"""
    try:
        payload = {'content': content, 'username': 'Stu'}
        if embed:
            payload['embeds'] = [embed.to_dict()]
        
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=payload) as resp:
                return resp.status == 204
    except Exception as e:
        print(f'Webhook error: {e}')
        return False

# Slash commands
@bot.tree.command(name='missions', description='Show active missions')
async def slash_missions(interaction: discord.Interaction):
    await interaction.response.defer()
    
    embed = discord.Embed(
        title='📋 Active Missions',
        color=0x00D4AA,
        timestamp=datetime.utcnow()
    )
    
    if active_missions:
        for mission in active_missions:
            embed.add_field(name=mission['name'], value=f"Agent: {mission['agent']}", inline=False)
    else:
        embed.description = 'No active missions'
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='agents', description='Show agent status')
async def slash_agents(interaction: discord.Interaction):
    embed = discord.Embed(
        title='🤖 Agent Fleet',
        color=0x00D4AA,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Stu', value='🟢 Online', inline=True)
    embed.add_field(name='FitBot', value='🟢 Online', inline=True)
    embed.add_field(name='SourceBot', value='🟢 Online', inline=True)
    embed.add_field(name='AuditBot', value='🟢 Online', inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='help', description='Show help')
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title='📖 Stu Help',
        description='Mention me or use slash commands',
        color=0x00D4AA
    )
    embed.add_field(name='Commands', value='/missions, /agents, /help', inline=False)
    await interaction.response.send_message(embed=embed)

# Sync slash commands
@bot.event
async def setup_hook():
    await bot.tree.sync()
    print('✅ Slash commands synced')

if __name__ == '__main__':
    if not TOKEN:
        print('❌ Error: Set STU_TOKEN environment variable')
        print('   export STU_TOKEN=your-token-here')
        exit(1)
    
    print('🚀 Starting Stu...')
    bot.run(TOKEN)
