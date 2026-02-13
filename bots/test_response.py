import discord
import os

TOKEN = os.getenv('STU_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Send test message to #general
    for guild in client.guilds:
        print(f'In guild: {guild.name}')
        for channel in guild.text_channels:
            if channel.name == 'general':
                try:
                    await channel.send('🔔 Test message from Stu — connection verified!')
                    print(f'Sent test message to #{channel.name}')
                except Exception as e:
                    print(f'Failed to send: {e}')

@client.event
async def on_message(message):
    print(f'Received message: {message.content} from {message.author}')
    if message.author == client.user:
        return
    if client.user in message.mentions:
        print(f'Bot mentioned! Responding...')
        await message.channel.send('👋 Stu here!')

client.run(TOKEN)
