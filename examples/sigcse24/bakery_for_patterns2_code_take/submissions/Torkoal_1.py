from bakery import assert_equal

def until_period(removeDot:list)->list:
    new_list = []
    for items in removeDot:
        if items == ".":
            new_list = removeDot
            new_list.remove(".")
            return new_list
assert_equal(until_period(["One", "Two", "."]), ["One", "Two"])
assert_equal(until_period(["One", "Two", "Three]), ["One", "Two","Three"])