from bakery import assert_equal
# assert_equal is imported from bakery
def is_expected_user(name: str, age: int, height: float) -> bool:
    return name == "Ada" and age == 1 and height == 11.7
''' 
This function gives the name, age, and height of a user and determines whether or
not it is true.

Args:
    name (str): The name of the user
    age (int): The age of the user
    height (float): The height of the user
Returns:
    bool: Whether or not the information is true
    '''
assert_equal(is_expected_user("Ada", 1, 11.7), True)
assert_equal(is_expected_user("Pumpkin", 4, 9.8), False)