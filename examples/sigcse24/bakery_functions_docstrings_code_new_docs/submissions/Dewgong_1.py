from cisc108 import assert_equal

def is_expected_user(name: str, age: int, height: float) -> bool:
       '''
        This function prints out the name, age, and height

        Args:
            name (str): The 
            age (int): how old the person is
            height (float): how tall the person is
        Returns:
            str: returns the name, age, and height
       '''
    return name == "Ada" and age == 1 and height == 11.7

assert_equal(is_expected_user("Ada", 1, 11.7), True)
assert_equal(is_expected_user("Pumpkin", 4, 9.8), False)