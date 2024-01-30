from bakery import assert_equal

def filter_scores(scores: list[int])->list[int]:
    #filter the scores
    New_Scores = []
    for score in scores:
        if score == -999:
            return New_Scores
        if score > 100:
            New_Scores.append(score)
    return New_Scores

def high_score(raw_scores: list[int])->int:
    scores = filter_scores(raw_scores)
    if not scores:
        return None
    max_s = scores[0]
    for score in score:
        if score > max_s:
    return max_s

assert_equal(filter_scores([1,-999,300]),[])
assert_equal(filter_scores([1,300,500]),[300,500])
assert_equal(filter_scores([1000,300,101]),[1000,300,101])

assert_equal(high_score([1,-999,300]),None)
assert_equal(high_score([300,200,3000]),3000)
assert_equal(high_score([101,3,54]),101)

    
            