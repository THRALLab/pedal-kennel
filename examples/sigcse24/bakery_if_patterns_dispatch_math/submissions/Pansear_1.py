from cisc108 import assert_equal
def dispatch_math(operator,num1,num2): # Function declaration
    if operator == '+': # if plus operator given then add num1 and num2
        return num1+num2
    elif operator == '-': # if minus operator given then subtract num1 and num2
        return num1-num2
    elif operator == '*': # if multiply operator given then multiply num1 by num2
        return num1*num2
    elif operator == '/': # if divide operator given then divide num1 by num2
        return num1/num2
    else:                 # else other operator given then return 0
        return 0
a = 5
b = 5
# Function call
print ("a + b = ",dispatch_math('+',a,b))
print ("a - b = ",dispatch_math('-',a,b))
print ("a * b = ",dispatch_math('*',a,b))
print ("a / b = ",dispatch_math('/',a,b))
print ("Anything else = ",dispatch_math('a',a,b))