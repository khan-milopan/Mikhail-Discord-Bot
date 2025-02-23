from disco import disco
import bot_select

def token(use_bot_selector:bool = False,
        force:bool = False,
        which_bot:int = -1):
    if use_bot_selector:
        return bot_select.select(force, which_bot)
    else:
        with open("bot_token.txt","r") as file:
            return f"{file.read()}"

bot = disco.Bot(f"{token(True, False, 0)}")

# My channel for testing (ignore if you're not me): 1332295313221750826