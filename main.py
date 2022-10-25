import telegram.ext as tele
import requests

app_id="809d4b86"
app_key="c0c4b9de2d7d3ed86774975bd604ac2a"
with open("token.txt", "r") as f:
    Token = f.read()

def input(update,context):
    word_id=update.message.text
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_id.lower()}"
    r = requests.get(url)
    update.message.reply_text(f"{r.text}")


def start(update, context):
    update.message.reply_text(
        "Hi, Welcome to Dictionary Bot!\nEnter a word to learn about its definition and much more."
    )
    
def main():
    updater = tele.Updater(Token, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(tele.CommandHandler('start',start))
    disp.add_handler(tele.MessageHandler(tele.Filters.text,input))

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()