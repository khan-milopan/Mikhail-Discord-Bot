# Mikhail

autoGenerateConfig = True # Disable this if you don't want for "config.py" to be created if missing

import os
import sys

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
            if autoGenerateConfig:
                with open("config.py","w") as file:
                    file.write(defaultConfig)
                raise SystemExit
            else:
                class config:
                    useMiloSelector = True
                    autoUpdateMiloSelector = True
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
            token = botSelect.select(True, 1)
        else:
            print('GENERATING "botTokens.json"!!!')
            botSelect.select()
            raise SystemExit
    else: # Use the .txt file
        if os.path.exists("botToken.txt"):
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

devC="DEVELOPER COMMAND - "

cog = bot.create_group("cog")

async def errorSend(ctx:discord.ApplicationContext, errorCode):
    await ctx.respond(f"**Error:**\n```\n{errorCode}\n```", ephemeral=True)

async def cogNotFound(ctx:discord.ApplicationContext):
    await ctx.respond(f"{cog} not found.", ephemeral=True)

@cog.command(description=devC+"Lists cogs.")
async def list(ctx:discord.ApplicationContext):
    try:
        cogs = os.listdir("./cogs")
        if "__pycache__" in cogs:
            cogs.remove("__pycache__")
        await ctx.respond(f"```{cogs}```", ephemeral=True)
    except Exception as errorCode:
        await errorSend(ctx, errorCode)

@cog.command(description=devC+"Loads cogs.")
async def load(
    ctx:discord.ApplicationContext,
    cog:discord.SlashCommandOptionType.string,
):
    try:
        if f"{cog}.py" in os.listdir("./cogs"):
            bot.load_extension(f"cogs.{cog}")
            await ctx.respond(f"Loaded {cog}.", ephemeral=True)
        else:
            await cogNotFound(ctx)
    except Exception as errorCode:
        await errorSend(ctx, errorCode)

@cog.command(description=devC+"Unloads cogs.")
async def unload(
    ctx:discord.ApplicationContext,
    cog:discord.SlashCommandOptionType.string,
):
    try:
        if f"{cog}.py" in os.listdir("./cogs"):
            bot.unload_extension(f"cogs.{cog}")
            await ctx.respond(f"Unloaded {cog}.", ephemeral=True)
        else:
            await cogNotFound(ctx)
    except Exception as errorCode:
        await errorSend(ctx, errorCode)

@cog.command(description=devC+"Reloads cogs.")
async def reload(
    ctx:discord.ApplicationContext,
    cog:discord.SlashCommandOptionType.string,
):
    try:
        if f"{cog}.py" in os.listdir("./cogs"):
            bot.reload_extension(f"cogs.{cog}")
            bot.load_extension(f"cogs.{cog}")
            await ctx.respond(f"Reloaded {cog}.", ephemeral=True)
        else:
            await cogNotFound(ctx)
    except Exception as errorCode:
        await errorSend(ctx, errorCode)

print("Running the bot...")
bot.run(token)
print("The bot has stopped running.")