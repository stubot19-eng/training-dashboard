#!/usr/bin/env python3
"""
SWARM OS - SourceBot
Procurement & Sourcing Agent
"""

import discord
import os
import aiohttp
from discord.ext import commands
from datetime import datetime

TOKEN = os.getenv('SOURCEBOT_TOKEN')
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1471913899329589420/bikMi7tgGGrVdgbTZ15_QC06N4viqFR20oqXgK1jTCiUKS_8ds-Sg4CNaRBMz1JRVogs'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='sb!', intents=intents, help_command=None)

# Mock procurement data
inventory = {
    'peptides': {'Reta': 'In stock', 'CJC/IPA': 'In stock'},
    'supplements': {'Whey Protein': 'Low stock', 'Creatine': 'In stock'},
    'equipment': {'Gym bag': 'In stock'}
}

@bot.event
async def on_ready():
    print(f'🟢 SourceBot is online! Logged in as {bot.user}')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name='for sourcing requests'),
        status=discord.Status.online
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user in message.mentions:
        await handle_mention(message)
        return
    
    content_lower = message.content.lower()
    if any(trigger in content_lower for trigger in ['sourcebot', 'source', 'buy', 'price', 'inventory']):
        if not message.content.startswith('sb!'):
            await handle_mention(message)
            return
    
    await bot.process_commands(message)

async def handle_mention(message):
    content = message.content
    for mention in message.mentions:
        content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
    content = content.strip()
    content_lower = content.lower()
    
    print(f'[SourceBot] Received: {content}')
    
    if any(word in content_lower for word in ['inventory', 'stock', 'what do we have']):
        await show_inventory(message.channel)
    
    elif any(word in content_lower for word in ['find', 'price', 'best price', 'search']):
        item = content.replace('find', '').replace('price', '').replace('search', '').strip()
        if item:
            await search_item(message.channel, item)
        else:
            await message.channel.send('🔍 What item should I search for?')
    
    elif any(word in content_lower for word in ['order', 'track', 'shipment']):
        await message.channel.send('📦 Order tracking: No active orders')
    
    elif any(word in content_lower for word in ['help', 'command']):
        await show_help(message.channel)
    
    else:
        await message.channel.send(
            f'👋 SourceBot here. I can help with:\n'
            f'• Inventory check\n'
            f'• Price searches\n'
            f'• Order tracking\n'
            f'• Vendor vetting'
        )

async def show_inventory(channel):
    embed = discord.Embed(
        title='📦 Current Inventory',
        color=0x00AAFF,
        timestamp=datetime.utcnow()
    )
    
    for category, items in inventory.items():
        value = '\n'.join([f'• {item}: {status}' for item, status in items.items()])
        embed.add_field(name=category.title(), value=value, inline=False)
    
    await channel.send(embed=embed)

async def search_item(channel, item):
    embed = discord.Embed(
        title=f'🔍 Searching: {item}',
        description='Price comparison across suppliers...',
        color=0x00AAFF
    )
    embed.add_field(name='Supplier A', value='$XX.XX (est)', inline=True)
    embed.add_field(name='Supplier B', value='$XX.XX (est)', inline=True)
    embed.add_field(name='Supplier C', value='$XX.XX (est)', inline=True)
    embed.set_footer(text='Detailed report posted to #sourcing')
    await channel.send(embed=embed)

async def show_help(channel):
    embed = discord.Embed(
        title='📖 SourceBot Help',
        description='Procurement & Sourcing Agent',
        color=0x00AAFF
    )
    embed.add_field(
        name='Commands',
        value='@SourceBot inventory\n@SourceBot find [item]\n@SourceBot track [order]\n@SourceBot vet [supplier]',
        inline=False
    )
    await channel.send(embed=embed)

@bot.tree.command(name='inventory', description='Show current inventory')
async def slash_inventory(interaction: discord.Interaction):
    embed = discord.Embed(title='📦 Inventory', color=0x00AAFF)
    for category, items in inventory.items():
        value = '\n'.join([f'{item}: {status}' for item, status in items.items()])
        embed.add_field(name=category.title(), value=value, inline=False)
    await interaction.response.send_message(embed=embed)

@bot.event
async def setup_hook():
    await bot.tree.sync()

if __name__ == '__main__':
    if not TOKEN:
        print('❌ Set SOURCEBOT_TOKEN environment variable')
        exit(1)
    print('🚀 Starting SourceBot...')
    bot.run(TOKEN)
