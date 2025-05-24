import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import Stop_Helper
import Route_Helper

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

PRINT_IN_GROUPS_OF = 1
MAX_CHAR_PRINT = 2000

DESCRIPTION_FLAG = "desc"

options = {
   "options": {
       DESCRIPTION_FLAG: "Displays available commands and descriptions"
   },
    "predict": {
       DESCRIPTION_FLAG: "Predict when a train will arrive"
   }
}

async def Group_Print_List(list, ctx):
    ind:int = 0
    while ind < len(list):
        to_print = ""
        while ind < len(list) and len(to_print) + len(list[ind]) < MAX_CHAR_PRINT:
            to_print += list[ind] + "\n"
            ind += 1
        await ctx.send(to_print)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name="options")
async def get_help(ctx):
    text = ""
    for option in options:
        text = "Command: \"" + option + "\" " + options[option][DESCRIPTION_FLAG] + "\n"
    await ctx.send(text)

@bot.command(name="predict")
async def pick_stop(ctx):
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    # filter route type
    route_types = Route_Helper.Get_Route_Types()
    await ctx.send("Please choose a route type:")
    await Group_Print_List(route_types, ctx)

    route_type = ""
    valid_input = False
    while not valid_input:
        try:
            response = await bot.wait_for("message", check=check, timeout=30.0)
            route_type = response.content.title()
            if Route_Helper.Type_Is_Valid(route_type):
                await ctx.send("You chose: " + route_type)
                valid_input = True
            else:
                await ctx.send("Invalid, enter a valid type")
        except asyncio.TimeoutError:
            await ctx.send("Timeout")
            return
    
    # filter route
    routes = Route_Helper.Get_List_Filter_Type(route_type)
    await ctx.send("Please choose a route:")
    await Group_Print_List(routes, ctx)

    route = ""
    valid_input = False
    while not valid_input:
        try:
            response = await bot.wait_for("message", check=check, timeout=30.0)
            route = response.content.title()
            if route in routes:
                await ctx.send("You chose: " + route)
                valid_input = True
            else:
                await ctx.send("Invalid, enter a valid route")
        except asyncio.TimeoutError:
            await ctx.send("Timeout")
            return

    # pick stop
    stops = Stop_Helper.Get_List_Filter_Route(route)
    await ctx.send("Please choose a stop:")
    await Group_Print_List(stops, ctx)

    stop = ""
    valid_input = False
    while not valid_input:
        try:
            response = await bot.wait_for("message", check=check, timeout=30.0)
            stop = response.content.title()
            if stop in stops:
                await ctx.send("You chose: " + stop)
                valid_input = True
            else:
                await ctx.send("Invalid, enter a valid stop")
        except asyncio.TimeoutError:
            await ctx.send("Timeout")
            return
    
    

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