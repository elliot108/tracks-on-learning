import math
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
    return s # return 

# this funciton returns the indeces of the same characters found in a string
# return False if the character is not found
def find_and_return_index(s, f):
    isFound = s.find(f)
    index = ()
    while isFound >= 0:
        index += isFound,
        isFound = s.find(f, isFound+1, len(s)-1)
    if index:
        if len(index)>1:
            return index
        else:
            return index[0]
    else:
        return False
    
# this function returns a string that has replaced the characters 
# with the string user provided
# 's' is a string that needs to be replaced
# 'r' is a string with which the user wants to replace the character
# '*i' is a tuple in which index numbers of characters that user wants to replace
def replace_by_index(s: str,r:str, *i:tuple):
    new_str = ""
    if len(i)>1:        
        new_str += s[:i[0]] + r
        index = 1
        while index < len(i):
            new_str += s[i[index-1]+1:i[index]] + r
            index += 1

        new_str += s.removeprefix(s[:i[len(i)-1]+1])
        return new_str
    else:
        print("work")
        new_str += s[:i[0]] + r
        new_str += s.removeprefix(s[:i[0]+1])
        print(new_str)
        return new_str

# this function is used to take user's input as string and evaluate it
# return a tuple (input and the result) if the input can be evaluated
# return a message if the input cannot be evaluated
def calculate(input):
    if input:  
        if input.find("^"):
            input = input.replace("^", "**") 
        if input.find("÷"):
            input = input.replace("÷", "/")
        if input.find("×"):
            input = input.replace("×", "*")

        if contains_Alpha_Or_SpecCha(input): #if the user's input contains alphabets or other characters that are not mathematical notations
            if containsTrigoSigns(input): # if the input has trigo signs
                try:
                    number_only = calculateTrigo(input) # calculate the trigo functions and store only numbers and operators
                except ValueError:
                    error_msg = "Invalid input for trigo function. \nPlease check your trigo signs and degree measures."
                    return error_msg
            else:
                # if the user's input contains an alphabet or something that's not a number or operator, invalid input message is sent
                error_msg = "Please enter numbers and operators only."
                return error_msg
        else:
            number_only = input # input has only numbers and operators

        try:
            result = eval(number_only) # evaluating the user's math problem 
        except (SyntaxError,NameError,TypeError,SyntaxWarning) as e: 
            print(e)
            # if the user's input cannot be evaluated
            if type(e) == TypeError:
                number_only = number_only.replace(")(", ")*(")
                try:
                    result = eval(number_only)
                    return number_only, result
                except TypeError:
                    print(number_only)
                    number_only_new = number_only[0]+ replace_by_index(number_only[1:],"*(", find_and_return_index(number_only[1:],"("))
                    result = eval(number_only_new)
                    return number_only_new,result

            error_msg = '''Please enter a meaningful mathematical expression.
                        \nMake sure there are at least two operands and one operator in the middle.
                        \nThere should be no operator alone at the end.
                        \nAlphabets or words except trigo signs are not accepted. 
                        \nRemember that I cannot understand some operators that may make sense to you. e.g, if you want to do division, use this '/' operator.
                        \nAnd please use '*' to multiply. i.e. sending (3)(9) will raise an error.
                        '''
            return error_msg

        return input,result
    
    else:
        message = "Enter a mathematical expression. I will compute it and send the result to you."
        return message