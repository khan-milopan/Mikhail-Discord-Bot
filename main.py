from disco import disco

def token(use_bot_selector:bool = False):
    if use_bot_selector:
        print ("Bot Selector not implemented yet... :3")
    else:
        with open("bot_token.txt","r") as file:
            return f"{file.read()}"

bot = disco.Bot(token())

bot.req.send_msg(1332295313221750826,"Oke, ide testonjara")
bot.ws.start()