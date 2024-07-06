import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters,InlineQueryHandler, CallbackContext
from uuid import uuid4
import necessary_functions as myFunctions

# to see when and why things don't work as expected 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# start command 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Welcome, I am here to assist you with Maths"
    await context.bot.send_message(update.effective_chat.id, message)

# help command 
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = '''
                I can help you calculate your math problems.
                \nNot only simple math problems, you can also solve trigonometric problems. 
                \nYou can control me by sending the command or just send me your numbers!
                \nYou can also solve a problem in any chat by calling @calculatorByElliott_bot!
                \n/calulate - compute the mathematical expression that the user enters
                \nSome operators that may be different to your understanding
                \nDivision - '/'
                \nMultiplication - '*'
                \nPower - '^' or '**'
                \nDivision but to retrieve remainder - '%'
                \nDivision but to retrieve quotient - '//'
                \nFor other operators, you can use normal signs. i.e. for addition, use '+'
                '''
            
    await context.bot.send_message(update.effective_chat.id, message)
    
# this funciton will be run when the user sends /calculate command
async def command_calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot 

    input = str("".join(context.args)).replace(" []", "").lower() # removing all spaces in the input
    response = myFunctions.calculate(input)

    if type(response) == tuple:
        input, result = response
        response = "The answer of '"+ str(input) + "' is " + str(result)
    
    await bot.send_message(chat_id, response)

# this will be run when the user mentions this bot's username
async def inline_calculate(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    input = str("".join(query)).replace(" ", "").lower() # removing all spaces in the input

    after_calculating = myFunctions.calculate(input)
    # if the query could be evaluated, after_calculating should be a tuple
    if type(after_calculating):
        result = str(after_calculating[1]) # this will be the result of the user's math problem
        message = result
    else:
        result = str(query) # the user's query will be reflected
        message = str(after_calculating)

    inline_response = [] 
    inline_response.append(
        InlineQueryResultArticle(
            id= str(uuid4()), #creating a random unique id
            title= "Calculate", #to show above the text box
            input_message_content=InputTextMessageContent(result),
            description = message
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, inline_response)

# thsi funciton will be run when the suer sends a message
async def msg_calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot
    input = str("".join(update.message.text)).replace(" []", "").lower() # removing all spaces in the input
    response = myFunctions.calculate(input)

    if type(response) == tuple:
        input, result = response
        response = "The answer of '"+ str(input) + "' is " + str(result)
    
    await bot.send_message(chat_id, response)

# unknown command handler 
async def unknown(update=Update, context = ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Sorry I do not understand this command")

if __name__ == "__main__":
    # to initiate telegram bot
    application = ApplicationBuilder().token("7490282882:AAGRs2KGK-NdUGZW5pmq-i-71BZzBDaMHes").build()

    # start command handler 
    start_cm_handler = CommandHandler("start", start)

    # help command handler 
    help_cm_handler = CommandHandler("help", help)

    # calculate command handler 
    calculate_cm_handler = CommandHandler("calculate", command_calculate)

    # calculate inlinequery handler
    calculate_inlinequery_handler = InlineQueryHandler(inline_calculate)

    # calculate message handler 
    calculate_msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), msg_calculate)

    # create unknown command handler 
    unknown_cmd_handler = MessageHandler(filters.COMMAND, unknown)

    # adding all handlers
    application.add_handlers([
        start_cm_handler,
        calculate_cm_handler, 
        help_cm_handler,
        calculate_inlinequery_handler,
        calculate_msg_handler,
        unknown_cmd_handler
        ])

    application.run_polling()