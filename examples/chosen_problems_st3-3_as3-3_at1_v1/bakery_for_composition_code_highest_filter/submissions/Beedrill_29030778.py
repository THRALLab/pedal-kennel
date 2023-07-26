from bakery import assert_equal

def high_score(scores: [int]) -> int:
    if [i for i in scores if i >= 100] == []:
        return None
    to_return = 100
    for score in scores:
        if score == -999:
            break
        elif score >= to_return:
            to_return = score
    return to_return


assert_equal(high_score([98, 100, 99, 101, -999, 102]), 101)
assert_equal(high_score([]), None)
assert_equal(high_score([70]), None)
            
    
            
            