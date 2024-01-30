from bakery import assert_equal

def find_fruit(fruits: list[str]) -> str:
    found = "fruitless"
    for fruit in fruits:
        if fruit[-1] == "e":
            found = fruit
        return found

assert_equal(find_fruit(["apple", "banana", "orange"]), "orange")
assert_equal(find_fruit(["banana", "orange", "apple"]), "apple")
assert_equal(find_fruit(["orange", "apple", "banana"]), "banana")