from bakery import assert_equal

def find_fruit(fruits: list[str]) -> str:
    found = "fruitless"
    for fruit in fruits:
        if fruit[-1] == "e" or "a":
            found = fruit
        return found

assert_equal(find_fruit(["apple", "banana", "orange"]), "orange")