from cisc108 import assert_equal

def make_pig_latin(word: str) -> str:
    if word[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return word + "ay"