import json
from sys import prefix
import discord 
import os
import requests
from dotenv import load_dotenv
from discord.ext import commands
import random
import wolframalpha
import logging

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

@bot.command(name="create-channel", help=" -- Create new channel with name")
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

@bot.command(name="question", help=" -- Ask me any academic question")
async def question(ctx, *question):
    question = " ".join(list(question))
    app_id = "E8H76X-T8V8UHPUY2"
    client = wolframalpha.Client(app_id)
    req = client.query(question)
    print("looking for answers.....")
    res = next(req.results).text
    await ctx.send(res)

@bot.command(name="weather", help="get weather by adding any city")
async def weather(ctx, *city):
    loc = " ".join(list(city).split(" "))
    apiKey = 'ea21c2ee64bf2fd0f38674dc16e62852'
    try:
        req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={apiKey}")
        data = json.loads(req.text)
        weather = {
        'weather': f"Atmosphere:  {data['weather'][0]['main']}",
            'country': f"Country:  {data['sys']['country']}",
            'location': f"City:  {data['name']}",
            'weatherDesc': f"Desc:  {data['weather'][0]['description']}",
            'temperature': f"Temp:  {round(data['main']['temp'] - 273.15)}°С",
            'humidity': f"Humidity:  {data['main']['humidity']}%",
            'feel': f"Feels like:  {round(data['main']['feels_like'] - 273.15)}°С",
            'windSpeed': f"Wind:  {data['wind']['speed']}km/h" 
        }
        msg = f"{'*'*20}\nWeather in {loc.title()}\n{'*'*20}\n"
        for i in weather:
            msg += weather[i] + "\n\n"
        await ctx.send(msg)
    except:
        logging.error("could not find weather on open weather")
        await ctx.send("Errm... couldn't find weather check spelling and/or try again 😬😬")

   
# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('hello'):
#         await message.channel.send('Hello friend!!')


bot.run(TOKEN)

