from bakery import assert_equal

def no_less_than_100(numbers:list[int])->list[int]:
    stitch=[]
    for number in numbers:
        if number>=100:
            stitch.append(number)
    return stitch

def maximum(numbers:list[int])->int:
    purple=numbers[0]
    for number in numbers:
        if purple<number:
            purple=number
    return purple

def
        
def high_score(numbers:list[int])->int:
    x=no_less_than_100(numbers)
    if not numbers:
        return None   
    taking=True
    lilo=[]
    for number in x:
    if number==-999:
        taking=False
    elif taking:   
        lilo.append(number)
    return maximum(lilo)
    
assert_equal(high_score([]), None)
assert_equal(high_score([99,2,101,100]), 101)
assert_equal(high_score([5,-999]), 0)
            
    