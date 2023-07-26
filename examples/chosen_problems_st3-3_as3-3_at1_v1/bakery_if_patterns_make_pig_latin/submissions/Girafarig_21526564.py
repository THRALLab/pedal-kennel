from cisc108 import assert_equal

def make_pig_latin(word: str) -> str:
    if word[0] in 'aeiou':
        return word + 'ay'
    return word[1:] + word[0] + 'ay'

assert_equal(make_pig_latin("hello"), "elloay")
assert_equal(make_pig_latin("arugula"), "arugulaay")
assert_equal(make_pig_latin("potato"), "otatopay")
assert_equal(make_pig_latin("green"), "reengay")
