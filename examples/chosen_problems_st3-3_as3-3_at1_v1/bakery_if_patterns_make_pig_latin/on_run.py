from pedal import *
from curriculum_sneks import ensure_functions_return, prevent_printing_functions
from curriculum_sneks.tests import ensure_cisc108_tests

prevent_printing_functions()
ensure_functions_return()

ensure_function('make_pig_latin', parameters=[str], returns=str)
ensure_function_call('make_pig_latin', at_least=3)
ensure_coverage(.9)
ensure_cisc108_tests(3)
ensure_called_uniquely('make_pig_latin', 3)
unit_test("make_pig_latin",
          ([""], "ay"),
          (["hour"], "ourhay"),
          (["our"], "ouray"),
          (["dog"], "ogday"),
          (["apple"], "appleay")
)