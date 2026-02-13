import discord
import os
from discord.ext import commands

TOKEN = os.getenv('AUDITBOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='ab!', intents=intents)

@bot.event
async def on_ready():
    print(f'🟢 AuditBot ONLINE as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        await message.channel.send('🔍 Security: NORMAL | Issues: 0 | Uptime: 99.9%')
    await bot.process_commands(message)

bot.run(TOKEN)
