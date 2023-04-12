import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import urllib.request
import replicate
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Scrivimi su cosa vuoi che ti genero il tuo Pokémon e io cercherò di fare il mio meglio!\nPer più informazioni usa il comando /info")
    logging.info(f"Ricevuto comando start da {update.effective_user.first_name}")

async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    richiesta = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Generando il Pokémon di " + richiesta + "...")
    logging.info(f"Ricevuto input ({richiesta}) per la generazione da {update.effective_user.first_name}")
    output = replicate.run(
        "lambdal/text-to-pokemon:3554d9e699e09693d3fa334a79c58be9a405dd021d3e11281256d53185868912",
        input={"prompt": richiesta}
    )
    logging.info(f"Ricevuto l'URL ({output[0]}) dell'immagine generata da {update.effective_user.first_name}")
    url = output[0]
    urllib.request.urlretrieve(url, "generazione.png")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("generazione.png", "rb"))
    os.remove("generazione.png")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Questo bot ideato da @Licantropo3392 genererà un Pokémon in base a ciò che gli andrai a scrivere.\nSi basa sul modello lambdal/text-to-pokemon che puoi trovare sul sito Replicate.")
    logging.info(f"Ricevuto comando info da {update.effective_user.first_name}")

async def err(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Oops, non conosco questo comando, se stavi cercando di farmi generare un Pokémon ricorda di non mettere lo slash, scrivilo come se fosse un messaggio normalissimo che mandi a un tuo amico perché altrimenti penserò che sia un comando!")
    logging.info(f"Ricevuto un comando inesistente da {update.effective_user.first_name}")
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler("info", info)
    gen_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), gen)
    err_handler = MessageHandler(filters.COMMAND, err)
    application.add_handler(start_handler)
    application.add_handler(info_handler)
    application.add_handler(gen_handler)
    application.add_handler(err_handler)

    application.run_polling()