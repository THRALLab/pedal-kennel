from cisc108 import assert_equal

def make_pig_latin(word: str)->str:
    vowels = ["A","E","I","O","U"]
    if not word:
        return "ay"
    elif word[0].upper() in vowels:
        return word + "ay"
    return word[1:] + word[0] + "ay"

assertequal(make_pig_latin(""),"ay")
assertequal(make_pig_latin("effort"),"effortay")
assertequal(make_pig_latin("make"),"akemay")
assertequal(make_pig_latin("word"),"ordway")
assertequal(make_pig_latin("award"),"awarday")