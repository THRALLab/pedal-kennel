from bakery import assert_equal
def high_score(List:list[int])-> int:
    max = List[0]
    cont_count = True
    for nums in List:
        if nums == -999:
            cont_count = False
            if nums >=100:
                max = nums
    return max

assert_equal(high_score([150, -999, 200]), 150)