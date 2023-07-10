from cisc108 import assert_equal

def is_expected_user(name: str, age: int, height: float) -> bool:
    return name == "Ada" and age == 1 and height == 11.7
"""
    The function will take the inputted name, age, and height, and test
    to see if it is true or false
    
    Args:
        name(str): the name should be equal to whatever we want
        age(int): Whatever age we want to input
        height(float): whatever value we want as the height
    Returns: 
    boolean: whether or not the values in the test are equal to what is supposed to be returned. 
   
        """
assert_equal(is_expected_user("Ada", 1, 11.7), True)
assert_equal(is_expected_user("Pumpkin", 4, 9.8), False)