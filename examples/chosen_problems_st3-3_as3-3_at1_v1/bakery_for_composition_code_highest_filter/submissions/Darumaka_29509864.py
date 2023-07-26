from bakery import assert_equal


def high_score (scores:list[int])->int:
    maximum=score[0]
    for score in scores:
        if score > maximum:
            if score < 100:
                return None 
            maximum=score
    return maximum

assert_equal(high_score([500,50]), 500)
       
        