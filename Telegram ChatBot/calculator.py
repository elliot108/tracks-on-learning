import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters,InlineQueryHandler, CallbackContext
from uuid import uuid4
import math

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
    message = "I can help you calculate your math problems.\n\n You can control me by sending these commands\n/calulate - compute the mathematical expression that the user enters"
    await context.bot.send_message(update.effective_chat.id, message)

# to check if the user's input contains only numbers and operators
def isClean(input):
    for c in input:
        if c in "abcdefghijklmnopqrstuvwxyz!@#$&_?,<>~`;:'\"\\|":
            return False
    return True

# to check if the user's mathematical expression includes trigonometry 
def containsTrigoSigns(input: str):
    if input.find("sin") or input.find("cos") or input.find("tan") or input.find("cot") or input.find("sec") or input.find("cos"):
        return True
    return False

def calculateTrigo(triSign, angle):
     if triSign == "sin":
          return math.sin(angle)
     elif triSign == "cos":
          return math.cos(angle)
     elif triSign == "tan":
          return math.tan(angle)
     elif triSign == "cot":
          return math.atan(angle)
     elif triSign == "sec":
          return math.acos(angle)
     elif triSign == "cosec":
          return math.asin(angle)
     
def detectTrigo(s):
    trigoSigns = ["sin", "cos", "tan", "cot", "sec", "cosec"]
    for t in trigoSigns:
        f = s.find(t)
        while not f == -1:
            # c = s.count(t)
            if not t == "cosec":
                index = f+3
            else:
                index = f + 5
            next_cha = s[index]
            if next_cha.isdigit():
                    angle_measure = next_cha
                    index = index + 1
                    while index < len(s):
                        next_cha = s[index]
                        if next_cha.isdigit():
                            angle_measure += next_cha
                            index += 1
                            continue
                        elif next_cha == ".":
                            if next_cha.find("."):
                                print("more than one decimal points in angle measurement behind " + t)
                                return 
                            angle_measure += next_cha
                            index += 1
                            continue
                        else:
                            break
                    trigo = t+angle_measure
                    s = s.replace(trigo, "("+trigo+")")
                    print(s)
                    angle_measure = eval(angle_measure)
                    radian = angle_measure * (math.pi/180)
                    print(radian)
                    
                    trigo_value = calculateTrigo(t, radian)
                    s = s.replace(trigo, str(trigo_value))

                    index+= 2

                    if index < len(s):
                        f = s.find(t, index)
                    else:
                        break        
            else:
                    print("no digit behind " + t) 
                    return        
    return s
    
# to calculate user's input 
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot 

    input = str("".join(context.args)).replace(" []", "").lower() # removing all spaces in the input

    if input:
        if containsTrigoSigns(input):
            try:
                input = detectTrigo(input)
            except ValueError:
                invalid_input = "There's something wrong with trigo."
                await bot.send_message(chat_id, invalid_input)
                return
        # if the user's input contains an alphabet or something that's not a number or operator, invalid input message is sent
        if not isClean(input):
            invalid_input = "Please enter numbers and operators only."
            await bot.send_message(chat_id, invalid_input)
            return
        
        input = input.replace("^", "**") 
        try:
            result = eval(input) # evaluating the user's math problem 
        except SyntaxError: 
            # if the user's input cannot be evaluated
            error_msg = "Please enter a meaningful mathematical expression. Make sure there are at least two operands and one operator in the middle"
            await bot.send_message(chat_id, error_msg)
            return
        
        await bot.send_message(chat_id, result)

        return

    message = "Now you can enter a mathematical expression. I will compute it and send the result to you."
    await bot.send_message(chat_id, message)
    return

if __name__ == "__main__":
    # to initiate telegram bot
    application = ApplicationBuilder().token("7490282882:AAGRs2KGK-NdUGZW5pmq-i-71BZzBDaMHes").build()

    # start command handler 
    start_cm_handler = CommandHandler("start", start)

    # help command handler 
    help_cm_handler = CommandHandler("help", help)

    # calculate command handler 
    calculate_cm_handler = CommandHandler("calculate", calculate)
    # adding all handlers
    application.add_handlers([
        start_cm_handler,
        calculate_cm_handler, 
        help_cm_handler
        ])

    application.run_polling()