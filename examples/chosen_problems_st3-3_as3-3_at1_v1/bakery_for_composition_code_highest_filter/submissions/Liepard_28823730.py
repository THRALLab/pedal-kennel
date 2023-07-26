from bakery import assert_equal

def high_score(integers: list[int]) -> int:
    highest = integers[0]
    if len(integers) > 0:
        for integer in integers:
            if integer == -999:
                return None
            if integer >= 100:
                if highest < integer:
                    highest = integer
        return highest