from bakery import assert_equal
def make_pig_latin(Word:str)->str:
    if Word[0] in "aeiouAEIOU":
        pig_latin = Word + "ay"
    elif Word[0] not in "aeiouAEIOU" and "":
        pig_latin = Word[1:] + Word[0] +"ay"
    else:
            pig_latin = "ay"
    return pig_latin

assert_equal(make_pig_latin("Fiammetta"), "iamettaFay")       
assert_equal(make_pig_latin(""), "ay")
assert_equal(make_pig_latin("Exusiai"), "Exusiaiay")
