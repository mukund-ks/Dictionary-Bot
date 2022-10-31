import datetime
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext
import requests
import random

with open("Token.txt", "r") as f:
    Token = f.read()


def daily(context: CallbackContext):
    with open("words.txt", "r") as a:
        word = random.choice(list(a))
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    request_dict = requests.get(url).json()

    try:
        example = request_dict[0]["meanings"][0]["definitions"][0]["example"]
    except:
        example = "Example not available."

    try:
        message = (
            "Word of the Day: "
            + word
            + "\nMeaning: "
            + request_dict[0]["meanings"][0]["definitions"][0]["definition"]
            + "Example: "
            + example
        )
        context.bot.send_message(text=message)
    except:
        message="An Error Occoured."
        context.bot.send_message(text=message)


def input(update, context):
    word_id = update.message.text
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_id.lower()}"
    r_dict = requests.get(url).json()
    try:
        update.message.reply_text(
            "Meaning: " + r_dict[0]["meanings"][0]["definitions"][0]["definition"]
        )
    except:
        update.message.reply_text("Invalid Word. Maybe check your spelling.")
        return
    try:
        update.message.reply_text(
            "Example: " + r_dict[0]["meanings"][0]["definitions"][0]["example"]
        )
    except:
        update.message.reply_text("Example not available.")


def start(update, context):
    update.message.reply_text(
        "Hi, Welcome to Dictionary Bot!\n\nEnter a word to get its definition and an example.\nI'll be texting you one random word everyday at 11 AM IST, with its definition and example obviously :)\n\n\nThis bot is a project of - https://github.com/mukund-ks"
    )


def main():
    updater = Updater(Token, use_context=True)
    disp = updater.dispatcher

    updater.job_queue.run_daily(
        daily,
        days=(0, 1, 2, 3, 4, 5, 6),
        time=datetime.time(hour=20, minute=30, second=00),
    )
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(MessageHandler(Filters.text, input))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
