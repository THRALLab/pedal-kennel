from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Recipe:
    flour:int
    eggs:int
    milk:int
    sugar:int
    
def merg_recipes(rec:Recipe, rec2:Recipe) -> Recipe:
     rec = Recipe(1,3,2,2)
         rec2 = Recipe(3,4,2,4):
            return rec + rec2