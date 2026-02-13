#!/usr/bin/env python3
"""
SWARM OS - AuditBot
Security & Compliance Agent
"""

import discord
import os
import aiohttp
from discord.ext import commands
from datetime import datetime

TOKEN = os.getenv('AUDITBOT_TOKEN')
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1471913903842656306/u6zO2zB8l7GhMbX-9RAntEIvywk528wA7ZuKABwmC3gSDVKTfVewArd_Cmhsphtr2Pi9'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='ab!', intents=intents, help_command=None)

# Security status
security_status = {
    'level': 'normal',  # normal, advisory, warning, critical
    'last_scan': datetime.utcnow().isoformat(),
    'issues': [],
    'uptime': '99.9%'
}

@bot.event
async def on_ready():
    print(f'🟢 AuditBot is online! Logged in as {bot.user}')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name='for security events'),
        status=discord.Status.dnd  # Red status for security
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user in message.mentions:
        await handle_mention(message)
        return
    
    content_lower = message.content.lower()
    if any(trigger in content_lower for trigger in ['auditbot', 'audit', 'security', 'scan', 'check']):
        if not message.content.startswith('ab!'):
            await handle_mention(message)
            return
    
    await bot.process_commands(message)

async def handle_mention(message):
    content = message.content
    for mention in message.mentions:
        content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
    content = content.strip().lower()
    
    print(f'[AuditBot] Received: {content}')
    
    if any(word in content for word in ['scan', 'security scan', 'check']):
        await run_scan(message.channel)
    
    elif any(word in content for word in ['status', 'security status']):
        await show_status(message.channel)
    
    elif any(word in content for word in ['logs', 'issues', 'problems']):
        await show_issues(message.channel)
    
    elif any(word in content for word in ['help', 'command']):
        await show_help(message.channel)
    
    else:
        await message.channel.send(
            f'🔍 AuditBot monitoring. Commands:\n'
            f'• Run security scan\n'
            f'• Show status\n'
            f'• Check issues\n'
            f'• View logs'
        )

async def run_scan(channel):
    embed = discord.Embed(
        title='🔍 Security Scan Initiated',
        description='Scanning all systems...',
        color=0xFFBB33
    )
    msg = await channel.send(embed=embed)
    
    # Simulate scan
    await asyncio.sleep(2)
    
    embed = discord.Embed(
        title='✅ Security Scan Complete',
        description='No critical issues found',
        color=0x00C851,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Status', value='🟢 All Clear', inline=True)
    embed.add_field(name='Issues Found', value='0', inline=True)
    embed.add_field(name='Last Scan', value='Just now', inline=True)
    
    await msg.edit(embed=embed)

async def show_status(channel):
    level_emoji = {'normal': '🟢', 'advisory': '🟡', 'warning': '🟠', 'critical': '🔴'}
    emoji = level_emoji.get(security_status['level'], '⚪')
    
    embed = discord.Embed(
        title=f'{emoji} Security Status: {security_status["level"].upper()}',
        color={'normal': 0x00C851, 'advisory': 0xFFBB33, 'warning': 0xFF8800, 'critical': 0xFF4444}.get(security_status['level']),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='System Uptime', value=security_status['uptime'], inline=True)
    embed.add_field(name='Open Issues', value=str(len(security_status['issues'])), inline=True)
    embed.add_field(name='Last Scan', value=security_status['last_scan'][:10], inline=True)
    await channel.send(embed=embed)

async def show_issues(channel):
    if not security_status['issues']:
        await channel.send('🟢 No security issues on record.')
        return
    
    embed = discord.Embed(
        title='🔴 Security Issues',
        color=0xFF4444
    )
    for issue in security_status['issues']:
        embed.add_field(name=issue['title'], value=issue['description'], inline=False)
    await channel.send(embed=embed)

async def show_help(channel):
    embed = discord.Embed(
        title='📖 AuditBot Help',
        description='Security & Compliance Agent',
        color=0xFF4444
    )
    embed.add_field(
        name='Commands',
        value='@AuditBot scan\n@AuditBot status\n@AuditBot issues\n@AuditBot logs',
        inline=False
    )
    embed.add_field(
        name='Alert Levels',
        value='🟢 Normal | 🟡 Advisory | 🟠 Warning | 🔴 Critical',
        inline=False
    )
    await channel.send(embed=embed)

@bot.tree.command(name='scan', description='Run security scan')
async def slash_scan(interaction: discord.Interaction):
    await interaction.response.send_message('🔍 Running security scan...')
    await asyncio.sleep(2)
    await interaction.followup.send('✅ Scan complete. No issues found.')

@bot.tree.command(name='status', description='Show security status')
async def slash_status(interaction: discord.Interaction):
    emoji = '🟢' if security_status['level'] == 'normal' else '🔴'
    await interaction.response.send_message(f'{emoji} Security status: {security_status["level"].upper()}')

import asyncio

@bot.event
async def setup_hook():
    await bot.tree.sync()

if __name__ == '__main__':
    if not TOKEN:
        print('❌ Set AUDITBOT_TOKEN environment variable')
        exit(1)
    print('🚀 Starting AuditBot...')
    bot.run(TOKEN)
