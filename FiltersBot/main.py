import logging

from telegram import Update, ForceReply, ParseMode, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Defaults

# Enable logging
TOKEN = "5136553285:AAEI3N--MIE8Fsx1WnTJ0lXroTqdDhahPoE"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    # update.message.reply_text(update.message.text)
    text = f"<code>{update.message.text}</code>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)



def photo_or_video(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('You sent photo or video')

def audio(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="You sent audio!")
    #context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)

    #HELP!!! Как сделать так, чтобы бот переслал мое же сообщение с аудио?!


def forward_photo_or_video(update: Update, context: CallbackContext) -> None:
    text = f"<b>You sent forward photo or video!</b>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def url_sent(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="you sent message with URL")



def put(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    key = 'key1'
    value = context.args[0]
    print(context.user_data)
    context.user_data[key] = value
    print(context.user_data)
    update.message.reply_text(key)


# /get key
def get(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    key = context.args[0]
    if key in context.user_data:
        update.message.reply_text(context.user_data[key])
    else:
        update.message.reply_text("Error")

# /number [key1] [x]
def number (update: Update, context: CallbackContext) -> None:
    key = context.args[0]
    x = context.args[1]
    if len(context.args) !=2:
        update.message.reply_text("Error")
    else:
        context.user_data[key] = x
        update.message.reply_text(f"{key} = {x}")
        print(context.user_data)

# /sum [key1] [key2]
def sum (update: Update, context: CallbackContext) -> None:
    key1 = context.args[0]
    key2 = context.args[1]
    print(key1, key2)
    if key1 in context.user_data and  key2 in context.user_data:
        update.message.reply_text(int(context.user_data[key1]) + int(context.user_data[key2]) )
    else:
        update.message.reply_text("Error")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    defaults = Defaults(parse_mode=ParseMode.HTML)

    updater = Updater(TOKEN, defaults=defaults)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("put", put))
    dispatcher.add_handler(CommandHandler("get", get))
    dispatcher.add_handler(CommandHandler("number", number))
    dispatcher.add_handler(CommandHandler("sum", sum))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.entity(MessageEntity.URL), url_sent))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.forwarded & (Filters.photo | Filters.video), forward_photo_or_video))
    dispatcher.add_handler(MessageHandler(Filters.photo | Filters.video, photo_or_video))
    dispatcher.add_handler(MessageHandler(Filters.audio, audio))
    
    

    # & - and
    # | - or
    # ~ - not
    # ^ - xor

    # Filters.text, Filters.video, Filters.photo, Filters.audio, Filters.document
    # Filters.forwarded
    # Filters.entity(MessageEntity.URL)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main() 