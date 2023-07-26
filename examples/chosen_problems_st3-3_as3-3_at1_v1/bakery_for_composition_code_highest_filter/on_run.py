from pedal import *
from curriculum_sneks import *

student.MAXIMUM_TEMPORARY_LENGTH = 50

suppress("algorithmic", "iterating_over_empty_list")
suppress("algorithmic", "multiple_return_types")
prevent_advanced_iteration(allow_for=True, allow_function={'max'})

prevent_printing_functions()
ensure_functions_return()
ensure_function('high_score', parameters=['[int]'], returns=int)
ensure_function_call('high_score', at_least=2)
ensure_coverage(.9)
ensure_cisc108_tests(3)
ensure_called_uniquely('high_score', 3)
unit_test('high_score',
             ([[101, 102, 103]], 103),
             ([[]], None),
             ([[300, 400, 200]], 400),
             ([[50, 20, 30, 100]], 100),
             ([[50, 20, 30]], None)
             )
unit_test("high_score",
             ([[100, 200, 300, -999]], 300),
             ([[300, 200, 100, -999]], 300),
             ([[300, 200, -999, 500, 400]], 300),
             ([[400, 200, -999, 100, 200]], 400),
             ([[-999, 400, 300, 50]], None),
             ([[-999]], None),
             ([[20, 40, 30, -999, 100]], None),
             ([[50, 200, -999, 50]], 200)
            )
