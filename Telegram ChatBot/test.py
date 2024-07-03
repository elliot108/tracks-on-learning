import telegram.ext as ext
ext.BaseHandler
from telegram.ext import ConversationHandler
import math
# def isOperator(cha):
#     for c in cha:
#         if c in "+-*/^":
#             return True
#     return False

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
# pi = math.pi

# print(s.isnumeric())

s = "tan1sss+*sdsec45s*in80*co+t60/sin90cos90-tan80tan20sin30"

s = detectTrigo(s)
print(s)

