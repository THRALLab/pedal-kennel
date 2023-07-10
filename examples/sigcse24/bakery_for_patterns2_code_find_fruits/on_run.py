from pedal import *
from curriculum_sneks import *

# Prevent temporary variables for long arguments
student.MAXIMUM_TEMPORARY_LENGTH = 50

suppress("algorithmic", "iterating_over_empty_list")
prevent_advanced_iteration(allow_for=True)
if not ensure_ast('For'):
    compliment("You have the For Loop!", label="have_for")
if not ensure_ast('If'):
    compliment("You have the If Statement!", label="have_if")
prevent_printing_functions()
ensure_functions_return()
ensure_function('find_fruit', parameters=['[str]'], returns='str')
ensure_function_call('find_fruit', at_least=2)
ensure_coverage(.9)
ensure_cisc108_tests(3)
ensure_called_uniquely('find_fruit', 3)
unit_test('find_fruit',
          ([["apple"]], "apple"),
          ([["orange"]], "orange"),
          ([["banana"]], "banana"),
          ([["steak"]], "fruitless"),
          ([["oranges"]], "fruitless"),
          ([["steak", "eggs"]], "fruitless"),
          ([["steak", "apple"]], "apple"),
          ([["steak", "eggs", "apple"]], "apple"),
          ([["steak", "eggs", "banana"]], "banana"),
          ([["steak", "eggs", "banana", "hot dog"]], "banana"),
          ([["steak", "eggs", "orange"]], "orange"),
          ([["steak", "apple", "orange"]], "orange"),
          ([["steak", "eggs", "orange", "pineapple", "banana"]], "banana"))
