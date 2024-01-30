from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Recipe:
    flour: int
    eggs: int
    milk: int
    sugar: int

def merge_recipes (rec1:Recipe, rec2:Recipe)->Recipe:
    return rec1.flour + rec2.flour, rec1.eggs + rec2.eggs, rec1.milk + rec2.milk, rec1.suagr rec2.sugar

assert_equal(merge recipies(1,2,1,3,1,2,3,2), 3,4,3,5)