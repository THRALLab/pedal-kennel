from bakery import assert_equal

def summate(values: [int]) -> int:
    total = 0
    for value in values:
        total = total + value
    return total

def count(values: [int]) -> int:
    total = 0
    for value in values:
        total = total + 1
    return total
def average (numbers:list)-> float:
    if numbers == []:
        return None
    _average = summate(numbers)/count(numbers)
    return _average
assert_equal(average([1, 2, 1]), 1.333333333333333)
assert_equal(average([]), None)


