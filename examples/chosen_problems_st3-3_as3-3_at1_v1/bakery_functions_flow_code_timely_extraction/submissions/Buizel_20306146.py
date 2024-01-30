from bakery import assert_equal

def is_before_noon(hour: int) -> bool:
    return hour <= 12

def is_past_dawn(hour: int) -> bool:
    return hour >= 5

def is_morning(hour: int) -> bool:
    return ___

assert_equal(is_morning(1), False)
assert_equal(is_morning(6), True)
assert_equal(is_morning(11), True)
assert_equal(is_morning(14), False)