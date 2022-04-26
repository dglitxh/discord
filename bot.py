import json
from sys import prefix
import discord 
import os
import requests
from dotenv import load_dotenv
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('GUILD')


def get_quote():
    print("searching........")
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)[0]
    return (f"{json_data['q']}\n  ~ {json_data['a']}")


@bot.event
async def on_ready():
    guild = discord.utils.find(lambda guild: guild.name == GUILD, bot.guilds)

    print("Yo we logged in as {0.user}".format(bot))
    print(f'{guild.name}(id: {guild.id})')

    print(f'Guild Members:')
    async for member in guild.fetch_members(limit=150):
        print(f" -{member.name}")
    
@bot.command(name="motivate", help="-- Responds with a motivational  quote")
async def motivator(ctx):
    quote = get_quote()
    print(quote)
    await ctx.send(quote)



@bot.command(name="flip-coin", help=" -- Flips a coin")
async def flip(ctx):
    coin_face = random.choice(["Head", "Tail"])
    await ctx.send(coin_face)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hello {member.name}, welcome to the XEVR server"
    )

@bot.command(prefix="create-channel" help=" -- Create new channel with name")
@commands.has_role("admin")
async def create_channel(ctx, channel_name="XEVR"):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('hello'):
#         await message.channel.send('Hello friend!!')


bot.run(TOKEN)
