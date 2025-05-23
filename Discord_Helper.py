import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DESCRIPTION_FLAG = "desc"

options = {
   "options": {
       DESCRIPTION_FLAG: "Displays available commands and descriptions"
   }
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name="options")
async def get_help(ctx):
    text = ""
    for option in options:
        text = "Command: \"" + option + "\" " + options[option][DESCRIPTION_FLAG] + "\n"
    await ctx.send(text)

@bot.command(name="alerts")
async def get_alerts(ctx):
    await ctx.send("alerts response")

@bot.command(name="routes")
async def get_routes(ctx):
    await ctx.send("Routes response")

def Run_Bot():  
    load_dotenv("key.env")
    token = str(os.getenv('DISCORD_BOT_TOKEN'))
    bot.run(token)