from pedal import *
from curriculum_sneks import *

# Prevent temporary variables for long arguments
student.MAXIMUM_TEMPORARY_LENGTH = 50

suppress("algorithmic", "iterating_over_empty_list")
suppress("algorithmic", "unused_variable")
prevent_advanced_iteration(allow_for=True)
if not ensure_ast('For'):
    compliment("You have the For Loop!", label="have_for")
if not ensure_ast('If'):
    compliment("You have the If Statement!", label="have_if")
prevent_printing_functions()
ensure_functions_return()
ensure_function('until_period', parameters=['[str]'], returns='[str]')
ensure_function_call('until_period', at_least=2)
ensure_coverage(.9)
ensure_cisc108_tests(3)
ensure_called_uniquely('until_period', 3)
unit_test('until_period',
          ([["A", "B", "."]], ["A", "B"]),
          ([["A", ".", "B"]], ["A"]),
          ([[".", "A", "B"]], []),
          ([["A", "B", ".", "C"]], ["A", "B"]),
          ([["A", ".", "C", "B"]], ["A"]),
          ([["Apple", "Banana", "Cucumber"]], ["Apple", "Banana", "Cucumber"]),
          ([["."]], []),
          ([[".", "A", "B"]], []))