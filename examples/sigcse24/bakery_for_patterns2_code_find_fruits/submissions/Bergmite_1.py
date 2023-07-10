from bakery import assert_equal

def find_fruit(foods: list[str]) -> str:
    result = "Missing"
    if not foods:
        return "fruitless"
    for food in foods:
        if food == "apple" or food == "orange" or food == "banana":
            result = food
        else:
            return "fruitless"
        return result

assert_equal(find_fruit(["banana","orange","apple"]), "apple")
assert_equal(find_fruit(["orange","orange","banana"]), "banana")
assert_equal(find_fruit(["banana","apple","orange"]), "orange")
assert_equal(find_fruit([]), "fruitless")

    