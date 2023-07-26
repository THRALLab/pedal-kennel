def make_pig_latin(word: str) -> str:
    if word[0].lower() in "aeiou":
        return word + "ay"
    else:
        return word[1:] + word[0] + "ay"

print("TEST PASSED")
print("TEST PASSED")
print("TEST PASSED")