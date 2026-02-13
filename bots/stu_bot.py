import discord
import os
from discord.ext import commands

TOKEN = os.getenv('STU_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🟢 Stu ONLINE as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='@mentions'))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        await message.channel.send('👋 Stu here! Commands: missions, agents, help')
    await bot.process_commands(message)

bot.run(TOKEN)
