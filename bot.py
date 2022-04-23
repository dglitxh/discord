import discord 
import os
from dotenv import load_dotenv


load_dotenv()
bot_client = discord.Client()

@bot_client.event
async def on_ready():
    print("Yo we logged in as {0.user}".format(bot_client))

@bot_client.event
async def on_message(message):
    if message.author == bot_client.user:
        return

    if message.content.startswith('hello' or 'Hello'):
        await message.channel.send('Hello friend!!')



bot_client.run(os.getenv('BOT_TOKEN'))