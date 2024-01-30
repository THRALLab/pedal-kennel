from bakery import assert_equal

def high_score(scores: list[int]) -> int:
    if not scores:
        return None
    highest_score = scores[0]
    taking = True
    for score in scores:
        if -999 == score:
            taking = False
        elif taking and score >= 100 and score > highest_score:
            highest_score = score
    if highest_score < 100:
        return None
    return highest_score

assert_equal(high_score([101, 150, 175, -10, 53]), 175)
assert_equal(high_score([52, 63]), None)
assert_equal(high_score([105, -999, 175, -10, 53]), 105)
assert_equal(high_score([]), None)