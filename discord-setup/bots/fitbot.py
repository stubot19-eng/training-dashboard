#!/usr/bin/env python3
"""
SWARM OS - FitBot
Health & Performance Agent
"""

import discord
import os
import aiohttp
from discord.ext import commands
from datetime import datetime

TOKEN = os.getenv('FITBOT_TOKEN')
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1471913851065995294/c2glIe8MoUyQ-93FphYVbF5nvyleiHXZTbpCSC497FXdtcl-qadbQa6_B2mUemgzKDD_'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='fb!', intents=intents, help_command=None)

# Mock data - replace with real data source
fitness_data = {
    'weight': 192,
    'goal': 185,
    'steps_today': 8432,
    'calories_today': 2150,
    'active_minutes': 45,
    'workouts_this_week': 4
}

@bot.event
async def on_ready():
    print(f'🟢 FitBot is online! Logged in as {bot.user}')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name='your health'),
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
    if any(trigger in content_lower for trigger in ['fitbot', 'fit', 'workout', 'health', 'weight']):
        if not message.content.startswith('fb!'):
            await handle_mention(message)
            return
    
    await bot.process_commands(message)

async def handle_mention(message):
    content = message.content
    for mention in message.mentions:
        content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
    content = content.strip().lower()
    
    print(f'[FitBot] Received: {content}')
    
    if any(word in content for word in ['stats', 'status', 'progress', 'weight']):
        await show_stats(message.channel)
    
    elif any(word in content for word in ['log', 'workout', 'exercise']):
        await message.channel.send('💪 Log your workout: What did you do today?')
    
    elif any(word in content for word in ['goal', 'target']):
        await show_goals(message.channel)
    
    elif any(word in content for word in ['meal', 'food', 'calories', 'eat']):
        await message.channel.send(f'🍽️ Today: {fitness_data["calories_today"]}/2600 calories')
    
    elif any(word in content for word in ['help', 'command']):
        await show_help(message.channel)
    
    else:
        await message.channel.send(
            f'👋 Hey Bryce! I\'m FitBot. Ask me about:\n'
            f'• Stats/Progress\n'
            f'• Log workout\n'
            f'• Goals\n'
            f'• Meals/Calories'
        )

async def show_stats(channel):
    embed = discord.Embed(
        title='💪 Fitness Stats',
        color=0x00CC41,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Weight', value=f'{fitness_data["weight"]} lbs (Goal: {fitness_data["goal"]} lbs)', inline=True)
    embed.add_field(name='Steps Today', value=f'{fitness_data["steps_today"]:,}', inline=True)
    embed.add_field(name='Active Minutes', value=str(fitness_data["active_minutes"]), inline=True)
    embed.add_field(name='Workouts This Week', value=str(fitness_data["workouts_this_week"]), inline=True)
    embed.add_field(name='Calories', value=f'{fitness_data["calories_today"]}/2600', inline=True)
    
    progress = ((fitness_data["goal"] / fitness_data["weight"]) * 100)
    embed.add_field(name='Progress', value=f'{progress:.1f}% to goal', inline=True)
    
    await channel.send(embed=embed)

async def show_goals(channel):
    embed = discord.Embed(
        title='🎯 Fitness Goals',
        color=0x00CC41,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Weight Target', value=f'{fitness_data["goal"]} lbs', inline=True)
    embed.add_field(name='Current', value=f'{fitness_data["weight"]} lbs', inline=True)
    embed.add_field(name='Remaining', value=f'{fitness_data["weight"] - fitness_data["goal"]:.1f} lbs', inline=True)
    embed.add_field(name='Daily Calories', value='2,600 (cut protocol)', inline=False)
    embed.add_field(name='Protein Target', value='230g', inline=True)
    embed.add_field(name='Protocol', value='Reta + CJC/IPA', inline=True)
    await channel.send(embed=embed)

async def show_help(channel):
    embed = discord.Embed(
        title='📖 FitBot Help',
        description='Health & Performance Agent',
        color=0x00CC41
    )
    embed.add_field(
        name='Commands',
        value='@FitBot stats\n@FitBot goals\n@FitBot log workout\n@FitBot meals',
        inline=False
    )
    await channel.send(embed=embed)

@bot.tree.command(name='stats', description='Show fitness stats')
async def slash_stats(interaction: discord.Interaction):
    embed = discord.Embed(title='💪 Fitness Stats', color=0x00CC41, timestamp=datetime.utcnow())
    embed.add_field(name='Weight', value=f'{fitness_data["weight"]} lbs', inline=True)
    embed.add_field(name='Steps', value=f'{fitness_data["steps_today"]:,}', inline=True)
    embed.add_field(name='Workouts', value=str(fitness_data["workouts_this_week"]), inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='goals', description='Show fitness goals')
async def slash_goals(interaction: discord.Interaction):
    embed = discord.Embed(title='🎯 Goals', color=0x00CC41)
    embed.add_field(name='Target', value=f'{fitness_data["goal"]} lbs', inline=True)
    embed.add_field(name='Current', value=f'{fitness_data["weight"]} lbs', inline=True)
    await interaction.response.send_message(embed=embed)

@bot.event
async def setup_hook():
    await bot.tree.sync()

if __name__ == '__main__':
    if not TOKEN:
        print('❌ Set FITBOT_TOKEN environment variable')
        exit(1)
    print('🚀 Starting FitBot...')
    bot.run(TOKEN)
