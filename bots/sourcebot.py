import discord
import os
from discord.ext import commands

TOKEN = os.getenv('SOURCEBOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='sb!', intents=intents)

@bot.event
async def on_ready():
    print(f'🟢 SourceBot ONLINE as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        await message.channel.send('📦 Inventory: Reta ✓ CJC/IPA ✓ | 12 briefs generated')
    await bot.process_commands(message)

bot.run(TOKEN)
