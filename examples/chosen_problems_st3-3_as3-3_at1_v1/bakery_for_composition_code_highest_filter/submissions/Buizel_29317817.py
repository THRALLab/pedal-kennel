from bakery import assert_equal

def high_score(scores: list[int]) -> int:
    high = scores[0]
    for score in scores:
        if score > high:
            high = score
    return high
        
