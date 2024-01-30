from pedal import *
from curriculum_sneks import ensure_functions_return, prevent_printing_functions
from curriculum_sneks.tests import ensure_cisc108_tests

prevent_printing_functions()
ensure_functions_return()

ensure_function('dispatch_math', parameters=[str, int, int], returns=int)
ensure_function_call('dispatch_math', at_least=3)
ensure_coverage(.9)
ensure_cisc108_tests(3)
ensure_called_uniquely('dispatch_math', 3)
unit_test("dispatch_math",
          (["+", 0, 0], 0),
          (["+", 50, 50], 100),
          (["+", 25, 100], 125),
          (["+", 100, 25], 125),
          (["-", 0, 0], 0),
          (["-", 50, 50], 0),
          (["-", 25, 100], -75),
          (["-", 100, 25], 75),
          (["*", 0, 0], 0),
          (["*", 5, 5], 25),
          (["*", 2, 10], 20),
          (["*", 10, 5], 50),
          (["/", 100, 25], 0),
          (["++", 100, 25], 0)
)