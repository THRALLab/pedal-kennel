from cisc108 import assert_equal

def make_pig_latin(word:str)->str:
    if word==""
        return "ay"
    elif word[0] in "aeiou":
        return word+"ay"
    else:
        return word[1:]+word[0]+"ay"
    
    
