import discord
import os
from discord.ext import commands

TOKEN = os.getenv('FITBOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='fb!', intents=intents)

@bot.event
async def on_ready():
    print(f'🟢 FitBot ONLINE as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        await message.channel.send('💪 Weight: 192lbs | Goal: 185lbs | Workouts: 4 this week')
    await bot.process_commands(message)

bot.run(TOKEN)
