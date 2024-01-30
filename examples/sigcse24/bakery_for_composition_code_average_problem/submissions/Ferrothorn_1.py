#from bakery import assert_equal

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

def average(inList:list[int])-> int:
    total = 0 
    average = (summate(total) + count(total))
        
    return summate(inList)/count(inList)
