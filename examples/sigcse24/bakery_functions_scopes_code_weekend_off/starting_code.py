from bakery import assert_equal

day_of_week = "Wednesday"
def cut_day():
    return day_of_week[:-3]

assert_equal(cut_day(), "Wednes")
assert_equal(cut_day(), "Thurs")
assert_equal(cut_day(), "Satur")