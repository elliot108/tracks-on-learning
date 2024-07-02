import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters,InlineQueryHandler
from uuid import uuid4

# to see when and why things don't work as expected 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Welcome, I am here to assist you with Maths"
    await context.bot.send_message(update.effective_chat.id, message)

# to check if the user's input contains only numbers and operators
def isArithExpression(input):
    for c in input:
        if c in "abcdefghijklmnopqrstuvwxyz!@#$&_?,<>~`;:'\"\\|":
            return False
    return True

# to calculate user's input 
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = "".join(context.args).replace(" []", "").lower() # removing all spaces in the input

    # if the user's input contains an alphabet or something that's not a number or operator, invalid input message is sent
    if not isArithExpression(input):
        invalid_input = "Please enter numbers and operators only."
        await context.bot.send_message(update.effective_chat.id, invalid_input)

    result = eval(input) # evaluating the user's math problem 
    await context.bot.send_message(update.effective_chat.id, result)

if __name__ == "__main__":
    # to initiate telegram bot
    application = ApplicationBuilder().token("7490282882:AAGRs2KGK-NdUGZW5pmq-i-71BZzBDaMHes").build()

    # create start command handler 
    start_cm_handler = CommandHandler("start", start)

    # create calculate command handler 
    calculate_cm_handler = CommandHandler("calculate", calculate)

    # adding all handlers
    application.add_handlers([start_cm_handler,calculate_cm_handler])

    application.run_polling()