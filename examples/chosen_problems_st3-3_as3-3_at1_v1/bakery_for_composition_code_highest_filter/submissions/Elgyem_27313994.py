from bakery import assert_equal
def high_score(scores: [int])->int:

max_num = scores[0]

mini = 100

empty_list = []

if scores == empty_list:
    return None
for score in scores:
    if score==-999:
        return max_num
    if score < mini:
        continue
    if score == -999:
        break
    if score > max_num:
        max_num = score
        return max_num

assert_equal(high_score([300, 40, 200, 150]), 300)

assert_equal(high_score([50, 100, 400, -999]), 400)

assert_equal(high_score([600, 800,]), 800)

assert_equal(high_score([300, 200, -999, 400]), 300)