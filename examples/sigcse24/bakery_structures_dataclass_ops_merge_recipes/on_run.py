from pedal import *
from curriculum_sneks import *
from dataclasses import dataclass

prevent_printing_functions()
ensure_functions_return()

@dataclass
class Recipe:
    flour: int
    eggs: int
    milk: int
    sugar: int

ensure_dataclass(Recipe, priority='instructor')
assert_is_instance(evaluate("Recipe"), type)

ensure_function('merge_recipes', 2, ['Recipe', 'Recipe'], 'Recipe')
ensure_function_callable('merge_recipes')

ensure_coverage(.9)
ensure_cisc108_tests(2)
ensure_function_call('Recipe', 2)
ensure_called_uniquely('merge_recipes', 2)

unit_test('merge_recipes', 
          ([call('Recipe', 1, 2, 3, 4), call('Recipe', 1, 2, 3, 4)], call('Recipe', 2, 4, 6, 8)),
          ([call('Recipe', 1, 2, 3, 4), call('Recipe', 4, 3, 2, 1)], call('Recipe', 5, 5, 5, 5)),
          ([call('Recipe', 1, 2, 3, 4), call('Recipe', 0, 0, 0, 0)], call('Recipe', 1, 2, 3, 4)),
          ([call('Recipe', 0, 0, 0, 0), call('Recipe', 1, 2, 3, 4)], call('Recipe', 1, 2, 3, 4)),
)
