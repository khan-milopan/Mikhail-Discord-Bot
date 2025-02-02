# Mikhail

import os
import sys
import asyncio

# Checks for arguments
for arg in sys.argv:
    if arg == "--debug" or arg == "-d":
        debugMode = True
        print("DEBUG MODE")
    else:
        debugMode = False

# Creates the error thingy stuff yea
def error(errorCode, kill:bool = False): # TODO: Make it so that the code doesn't shit itself upon error
    if debugMode == True:
        print(errorCode)
    else:
        print('There was an error. Run in debug for more info.')
    if kill:
        raise SystemExit

try:
    import requests
except Exception as errorCode:
    error(errorCode)

# Config
defaultConfig = "useMiloSelector = True\nautoUpdateMiloSelector = False"
try:
    if os.path.exists("config.py"):
        import config
    else:
        with open("config.py","w") as file:
            file.write(defaultConfig)
        raise SystemExit
except Exception as errorCode:
    error(errorCode)

# Importing Pycord
try:
    import discord
except Exception as errorCode:
    error(errorCode)

# Token Selector
useTokenTxt = False
def downloadMiloSelector():
    rawMiloSelector = requests.get("https://raw.githubusercontent.com/khan-milopan/Discord-Bot-Token-Selector/refs/heads/main/botSelect.py")
    if rawMiloSelector.status_code == 200:
        with open("botSelect.py", "wb") as file:
            file.write(rawMiloSelector.content)
try:
    if config.useMiloSelector: # Use Milo's Selector
        if config.autoUpdateMiloSelector:
            downloadMiloSelector()
        if os.path.exists("botSelect.py"):
            import botSelect
        else:
            downloadMiloSelector()
            import botSelect
        if os.path.exists("botTokens.json") or os.path.exists("bot_tokens.json"):
            token = botSelect.select(True, 0)
        else:
            print('GENERATING "botTokens.json"!!!')
            botSelect.select()
            raise SystemExit
    elif os.path.exists("botToken.txt"): # Use the .txt file
        with open("botToken.txt","r") as file:
            token = file.read()
    else:
        with open("botToken.txt","w") as file:
            file.write("Enter your bot token here")
            raise SystemExit
except Exception as errorCode:
    error(errorCode)

# PyCord thingys
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"I logged in as \"{bot.user}\".")
    if not config.customStatus == "":
        customStatus=discord.CustomActivity(name=config.customStatus)
        await bot.change_presence(activity=customStatus)
        print(f"Status set to \"{customStatus}\".")

devC="DEVELOPER COMMAND - "

cog = bot.create_group("cog")

async def errorSend(ctx:discord.ApplicationContext, errorCode):
    if debugMode:
        await ctx.respond(f"**There was an error**\n```traceback\n{errorCode}\n```", ephemeral=True)
    else:
        await ctx.respond(f"**There was an error**", ephemeral=True)

async def cogNotFound(ctx:discord.ApplicationContext):
    await ctx.respond(f"{cog} not found.", ephemeral=True)

async def accessCheck(
    ctx:discord.ApplicationContext,
    password:str,
    autoRespond:bool = False
    ):
    if ctx.channel.id in config.terminalChannels:
        return True
    elif password in config.adminPassword:
        return True
    else:
        if autoRespond:
            await ctx.respond("Access denied.", ephemeral=True)
        return False

@cog.command(description=devC+"Lists cogs.")
async def list(
    ctx:discord.ApplicationContext,
    password:discord.SlashCommandOptionType.string = None
    ):
    if await accessCheck(ctx, password, True):
        try:
            cogs = os.listdir("./cogs")
            if "__pycache__" in cogs:
                cogs.remove("__pycache__")
            await ctx.respond(f"```{cogs}```", ephemeral=True)
        except Exception as errorCode:
            await errorSend(ctx, errorCode)
            error(errorCode)

@cog.command(description=devC+"Loads cogs.")
async def load(
    ctx:discord.ApplicationContext,
    cog:discord.SlashCommandOptionType.string,
    password:discord.SlashCommandOptionType.string = None
    ):
    if await accessCheck(ctx, password, True):
        try:
            if f"{cog}.py" in os.listdir("./cogs"):
                bot.load_extension(f"cogs.{cog}")
                await ctx.respond(f"Loaded {cog}.", ephemeral=True)
            else:
                await cogNotFound(ctx)
        except Exception as errorCode:
            await errorSend(ctx, errorCode)
            error(errorCode)

@cog.command(description=devC+"Unloads cogs.")
async def unload(
    ctx:discord.ApplicationContext,
    cog:discord.SlashCommandOptionType.string,
    password:discord.SlashCommandOptionType.string = None
    ):
    if await accessCheck(ctx, password, True):
        try:
            if f"{cog}.py" in os.listdir("./cogs"):
                bot.unload_extension(f"cogs.{cog}")
                await ctx.respond(f"Unloaded {cog}.", ephemeral=True)
            else:
                await cogNotFound(ctx)
        except Exception as errorCode:
            await errorSend(ctx, errorCode)
            error(errorCode)

@cog.command(description=devC+"Reloads cogs.")
async def reload(
    ctx:discord.ApplicationContext,
    cog:discord.SlashCommandOptionType.string,
    password:discord.SlashCommandOptionType.string = None
    ):
    if await accessCheck(ctx, password, True):
        try:
            if f"{cog}.py" in os.listdir("./cogs"):
                bot.reload_extension(f"cogs.{cog}")
                bot.load_extension(f"cogs.{cog}")
                await ctx.respond(f"Reloaded {cog}.", ephemeral=True)
            else:
                await cogNotFound(ctx)
        except Exception as errorCode:
            await errorSend(ctx, errorCode)
            error(errorCode)

# Automatic cog loading
cogIgnore=[]
for file in os.listdir("./cogs"):
    if file.endswith(".py") and file not in cogIgnore:
        try:
            bot.load_extension(f"cogs.{file}")
            print(f"Loaded {file}")
        except Exception as errorCode:
            print(f"Failed to load {file}")
            error(errorCode)

print("Running the bot...")
bot.run(token)
print("\nThe bot has stopped running.")