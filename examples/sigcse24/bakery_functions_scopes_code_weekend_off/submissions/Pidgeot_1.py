from bakery import assert_equal

day_of_week = "Wednesday"
def cut_day(day_of_week:str= "Wednesday" or "Thursday" or "Saturday")->str:
    return day_of_week[:-3]

assert_equal(cut_day(day_of_week = "Wednesday"), "Wednes")
assert_equal(cut_day(day_of_week = "Thursday"), "Thurs")
assert_equal(cut_day(day_of_week = "Saturday"), "Satur")