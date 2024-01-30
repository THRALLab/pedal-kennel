from bakery import assert_equal

def is_expected_user(name: str, age: int, height: float) -> bool:
    return name == "Ada" and age == 1 and height == 11.7

assert_equal(is_expected_user("Ada", 1, 11.7), True)
assert_equal(is_expected_user("Pumpkin", 4, 9.8), False)