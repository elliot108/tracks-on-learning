import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters,InlineQueryHandler
from uuid import uuid4
# to see when and why things don't work as expected 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# what to do when the user hits start command 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update contains the information from user
    # context contains the information from the bot
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello World")

# echoing user's message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# send all caps of user's message 
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_caps = str(context.args).upper() # take only the arguments (not the command itslef) and caps them all
    await context.bot.send_message(chat_id= update.effective_chat.id, text=all_caps)

# inline query 
async def inline_caps(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    results = [] 

    results.append(
        InlineQueryResultArticle(
            id= str(uuid4()),
            title= "CAPS",
            input_message_content=InputTextMessageContent(query.upper())
        )
    )

# unknown command handler 
async def unknown(update=Update, context = ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Sorry I do not understand this command")
if __name__ == "__main__":
    # build an application but this does not start running the bot 
    application = ApplicationBuilder().token("7431977160:AAG7mgVuOeHfhKBuSn_OPJozEAUHf5Ad6dM").build()

    # creating a start command 
    handler = CommandHandler('start', start)
    application.add_handler(handler)

    # create echo command  
    echo = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    #                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #                   take only text from user, not command 
    application.add_handler(echo)

    # create CAPS command 
    caps = CommandHandler('caps', caps)
    application.add_handler(caps)

    # create inline handler 
    inline_caps_handler = InlineQueryHandler(inline_caps)
    application.add_handler(inline_caps_handler)

    # create unknown command handler 
    unknown_cmd_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_cmd_handler)

    # start running the bot 
    application.run_polling()