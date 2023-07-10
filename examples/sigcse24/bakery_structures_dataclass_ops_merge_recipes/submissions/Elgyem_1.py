from dataclasses import dataclass
from bakery import assert_equal
@dataclass
class Recipe:
    flour: int
    eggs: int
    milk:int
    sugar:int
    
def merge_recipes(rec:Recipe,re:Recipe)->Recipe:
    new=Recipe(rec.flour+re.flour,rec.eggs+re.eggs,rec.milk+re.milk,rec.sugar+re.sugar)
    return new
rec= Recipe(1,2,2,3)
re= Recipe(2,2,2,3)
assert_equal(merge_recipes(rec,re),Recipe(3,4,4,6))
rec= Recipe(2,2,2,3)
re= Recipe(2,2,2,3)
assert_equal(merge_recipes(rec,re),Recipe(4,4,4,6))