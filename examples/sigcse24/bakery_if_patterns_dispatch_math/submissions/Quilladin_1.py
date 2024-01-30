from bakery import assert_equal


def dispatch_math(word:str, one:int, two:int,) -> str:
    if word == "+":
        return one + two
    if word == "-":
        return one - two
    if word == "*":
        return one * two
    if word == "/":
        return 0
    
assert_equal(dispatch_math("+", 2, 3), 5)
assert_equal(dispatch_math("-", 2, 3), -1)
assert_equal(dispatch_math("*", 2, 3), 6)
assert_equal(dispatch_math("/", 2, 3), 0)
