from bakery import assert_equal
def until_period(examples: list[str]) -> list[str]:
    taking = False
    first_examples = []
    for example in examples:
        if example == ".":
            taking = True
        elif taking:
            first_examples.append(example)
        return examples
assert_equal(until_period(["Oh", "Hello", "There."]), ["Oh", "Hello", "There."])
assert_equal(until_period(["Kind", "Heart", "Money."]), ["Kind", "Heart", "Money."])
assert_equal(until_period(["Money", "Water", "Food"]), ["Money", "Water", "Food"])
assert_equal(until_period(