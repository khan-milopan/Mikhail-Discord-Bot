import json

def select(force:bool=False, which_bot:int=-1):
    default_json = [
        {"Bot Name 1": "Token 0"},
        {"Bot Name 2": "Token 1"},
        {"These are just": "Token 2"},
        {"bot names that": "Token 3"},
        {"only you see": "Token 4"},
        {"from your terminal": "Token 5"},
        {"can be anything": "Token 6"}
    ]

    def confirm(bot_number:int, bot_name:list):
        answer_confirm = input(f'You have selected "{bot_name[bot_number]}", is this the right choice? (Y/N) ')
        if answer_confirm.lower() == "y":
            return True
        elif answer_confirm.lower() == "n":
            return False
        else:
            print("Invalid answer.")

    def ask_which_bot(bot_count:int, bot_list:str):
        error_no_bot = f"\nNo bot goes by that number!\n"
        while True:
            try:
                print(f"Which bot to select:\n{bot_list}")
                bot_number = int(input("Enter the number: "))
                if (bot_number > -1) and (bot_number < bot_count+1):
                    return bot_number
                else:
                    print(error_no_bot)
            except ValueError:
                print(error_no_bot)

    try:
        with open("bot_tokens.json", "r") as bot_tokens_file: # Check camelCase first
            raw_tokens = json.load(bot_tokens_file)
    except FileNotFoundError:
        try:
            with open("botTokens.json", "r") as bot_tokens_file: # Only if no camelCase check snake_case (Because backwards compatibility blah blah)
                raw_tokens = json.load(bot_tokens_file)
        except FileNotFoundError:
            with open("bot_tokens.json", "w") as bot_tokens_file:
                json.dump(default_json, bot_tokens_file, indent=4)
                raise SystemExit('"bot_tokens.json" file was created. Please place your tokens in there and try again.')
                
    bot_name = [list(obj.keys())[0] for obj in raw_tokens]
    bot_token = [list(obj.values())[0] for obj in raw_tokens]

    bot_list=""
    bot_count=-1
    for name in bot_name:
        bot_count += 1
        bot_list += f'   ({bot_count}) "{name}"'
        if name == bot_name[-1]:
            bot_list += "?"
        else:
            bot_list += f", \n"

    if which_bot < -1 and which_bot > bot_count:
        raise SystemExit(f"Invalid bot number. Please select a bot from 0 to {bot_count}.")
    elif force == False and which_bot == -1:
        while True:
            bot_number = ask_which_bot(bot_count, bot_list)
            if confirm(bot_number, bot_name):
                return f"{bot_token[bot_number]}"
    elif force == False and which_bot != -1:
        while True:
            confirm_bool=confirm(which_bot, bot_name)
            if confirm_bool:
                return f"{bot_token[which_bot]}"
            elif confirm_bool == False:
                break
        while True:
            bot_number = ask_which_bot(bot_count, bot_list)
            if confirm(bot_number, bot_name):
                return f"{bot_token[bot_number]}"
    elif force == True and which_bot != -1:
        return f"{bot_token[which_bot]}"
    elif force == True and which_bot == -1:
        return f"{bot_token[ask_which_bot(bot_count, bot_list)]}"
    else:
        raise SystemExit("Something went wrong.")

# By Milopan
# https://github.com/khan-milopan/Discord-Bot-Token-Selector
