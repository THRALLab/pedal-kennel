from cisc108 import assert_equal
def make_pig_latin(word:str)->str:
     if word[0].lower()in "aeiou"
        return word+"ay"
    else
        return word[1:]+word[0]+"ay"
        
assert_equal(make_pig_latin(word),ordway)