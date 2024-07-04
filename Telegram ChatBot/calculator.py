import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup
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

# to check if the user's input contains alphabets or other characters that are not mathematical notations
def contains_Alpha_Or_SpecCha(input):
    for c in input:
        if c in "abcdefghijklmnopqrstuvwxyz!@#$&_?,<>~`;:'\"\\|":
            return True
    return False

# to check if the user's mathematical expression includes trigonometry 
def containsTrigoSigns(input: str):
    if input.find("sin") or input.find("cos") or input.find("tan") or input.find("cot") or input.find("sec") or input.find("cos"):
        return True
    return False

# to compute Trigonometry functions
def computeTrigo(triSign, angle):
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

# a funciton to handle trogonometric expressions from user
def calculateTrigo(input):
    print(input)
    s = input # user's input will not be changed, only 's' will be changed later
    trigoSigns = ["sin", "cosec", "cos", "tan", "cot", "sec"]
    isEnclosed = False # a flag to indicate if the degree is enclosed behind trigo sign
    # find each sign of trigo in the input
    for t in trigoSigns:
        f = s.find(t)
        while not f == -1:
            if not t == "cosec":
                index = f+3
            else:
                index = f + 5

            next_cha = s[index]

            # check if next character is a number
            if next_cha.isdigit():
                    angle_measure = next_cha
                    index += 1
            # check if the degree or angle behind trigo is enclosed in brackets
            elif next_cha == "(":
                    isEnclosed = True
                    angle_measure = s[index+1]
                    print(angle_measure)
                    index += 2
            else:
                print("no degree behind " + t) 
                return s
            
            # collecting the degree or angle measure described after trigo sign
            while index < len(s):
                        next_cha = s[index]
                        if next_cha.isdigit():
                            angle_measure += next_cha #add subsequent numbers as angle to compute trigo function
                            index += 1
                            continue

                        elif next_cha == ".":
                            if next_cha.find("."):
                                print("more than one decimal points in angle measurement behind " + t)
                                return s
                            angle_measure += next_cha
                            index += 1
                            continue
                        else:
                            break
            
            # enclosing trigo functions so it will be easier to compute
            # e.g. sin80 => (sin80) or sin(30) => (sin30)
            trigo = ""
            if isEnclosed:
                 trigo = t + "("+ angle_measure + ")"
                 s = s.replace(trigo, t+angle_measure)
            trigo = t+angle_measure
            print(trigo)
            s = s.replace(trigo, "("+trigo+")")
            print(s)

            # computing trigo functions
            angle_measure = eval(angle_measure) # from string to number
            radian = math.radians(angle_measure) # from degree to radian 
            trigo_value = computeTrigo(t, radian)
            s = s.replace(trigo, str(trigo_value))

            index+= 2

            if index < len(s):
                f = s.find(t, index)
            else:
                break                                   
    return s
    
# this funciton will be run when the user sends /calculate commands
async def command_calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot 

    input = str("".join(context.args)).replace(" []", "").lower() # removing all spaces in the input

    if input:
        if contains_Alpha_Or_SpecCha(input): #if the user's input contains alphabets or other characters that are not mathematical notations
            if containsTrigoSigns(input): # if the input has trigo signs
                try:
                    input = calculateTrigo(input)
                except ValueError:
                    invalid_input = "Invalid input for trigo function. \nPlease check your trigo signs and degree measures."
                    await bot.send_message(chat_id, invalid_input)
                    return
            else:
                # if the user's input contains an alphabet or something that's not a number or operator, invalid input message is sent
                invalid_input = "Please enter numbers and operators only."
                await bot.send_message(chat_id, invalid_input)
                return
                
        input = input.replace("^", "**") 
        try:
            result = eval(input) # evaluating the user's math problem 
        except (SyntaxError,NameError,TypeError) as e: 
            # if the user's input cannot be evaluated
            if type(e) == TypeError:
                error_msg = '''Please enter a meaningful mathematical expression.                     
                            \nRemember that I cannot understand some operators that may make sense to you. e.g, if you want to do division, use this '/' operator.
                            \nAnd please use '*' to multiply. i.e. sending (3)(9) will raise an error.
                            '''
            error_msg = '''Please enter a meaningful mathematical expression.
                        \nMake sure there are at least two operands and one operator in the middle.
                        \nThere should be no operator alone at the end.
                        \nAlphabets or words except trigo signs are not accepted. 
                        \nRemember that I cannot understand some operators that may make sense to you. e.g, if you want to do division, use this '/' operator.
                        '''
            await bot.send_message(chat_id, error_msg) 
            return   

        await bot.send_message(chat_id, result)
        
    else:
        message = "Now you can enter a mathematical expression. I will compute it and send the result to you."
        await bot.send_message(chat_id, message)
        
# inline query to calculate
# this will be run when the user mentions this bot's username
async def inline_calculate(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    print(query)
    response = "" # this will be the result of the user's math problem
    message = "" # this will the message that can be seen while typing in telegram
    input = str("".join(query)).replace(" ", "").lower() # removing all spaces in the input
    print(input)
    if input:
        if contains_Alpha_Or_SpecCha(input): #if the user's input contains alphabets or other characters that are not mathematical notations
            if containsTrigoSigns(input): # if the input has trigo signs
                try:
                    input = calculateTrigo(input)
                except ValueError:
                    invalid_input = "Invalid input for trigo function"
                    response = query
                    message = invalid_input
                    return
            else:
                # if the user's input contains an alphabet or something that's not a number or operator, invalid input message is sent
                invalid_input = "Please enter numbers and operators only."
                response = query
                message = invalid_input
                return
                
        input = input.replace("^", "**") 
        try:
            result = eval(input) # evaluating the user's math problem 
            response = result
            message = str(result)
        except (SyntaxError,NameError,TypeError): 
            # if the user's input cannot be evaluated
                invalid_input = 'Please enter a meaningful mathematical expression.'
                response = query
                message = invalid_input        
    else:
        response = "NO INPUT"
        message = "What do you want to calculate?"

    results = [] 
    results.append(
        InlineQueryResultArticle(
            id= str(uuid4()), #creating a random unique id
            title= "Calculate", #to show above the text box
            input_message_content=InputTextMessageContent(response),
            description = message
        )
    )

    await context.bot.answer_inline_query(update.inline_query.id, results)

async def msg_calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot
    input = str("".join(update.message.text)).replace(" []", "").lower() # removing all spaces in the input

    if input:
        if contains_Alpha_Or_SpecCha(input): #if the user's input contains alphabets or other characters that are not mathematical notations
            if containsTrigoSigns(input): # if the input has trigo signs
                try:
                    input = calculateTrigo(input)
                except ValueError:
                    invalid_input = "Invalid input for trigo function. \nPlease check your trigo signs and degree measures."
                    await bot.send_message(chat_id, invalid_input)
                    return
            else:
                # if the user's input contains an alphabet or something that's not a number or operator, invalid input message is sent
                invalid_input = "Please enter numbers and operators only."
                await bot.send_message(chat_id, invalid_input)
                return
                
        input = input.replace("^", "**") 
        try:
            result = eval(input) # evaluating the user's math problem 
        except (SyntaxError,NameError,TypeError) as e: 
            # if the user's input cannot be evaluated
            if type(e) == TypeError:
                error_msg = '''Please enter a meaningful mathematical expression.                     
                            \nRemember that I cannot understand some operators that may make sense to you. e.g, if you want to do division, use this '/' operator.
                            \nAnd please use '*' to multiply. i.e. sending (3)(9) will raise an error.
                            '''
            error_msg = '''Please enter a meaningful mathematical expression.
                        \nMake sure there are at least two operands and one operator in the middle.
                        \nThere should be no operator alone at the end.
                        \nAlphabets or words except trigo signs are not accepted. 
                        \nRemember that I cannot understand some operators that may make sense to you. e.g, if you want to do division, use this '/' operator.
                        '''
            await bot.send_message(chat_id, error_msg) 
            return   

        await bot.send_message(chat_id, result)
        
    else:
        message = "Now you can enter a mathematical expression. I will compute it and send the result to you."
        await bot.send_message(chat_id, message)

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