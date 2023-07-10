from cisc108 import assert_equal

def cut_day(day_of_week):
    return day_of_week[:-3]

assert_equal(cut_day("Wednesday"), "Wednes")
assert_equal(cut_day("Thursday"), "Thurs")
assert_equal(cut_day("Saturday"), "Satur")