# Импортируем все необходимое
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext

import logging

TOKEN = "5136553285:AAEI3N--MIE8Fsx1WnTJ0lXroTqdDhahPoE"

updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def start (update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Hello")
    print (update)
    print (context)

def echo(update, context):
    text = 'Сам ты ' + update.message.text 

    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=text)  

start_handler = CommandHandler('start', start) # /start
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()