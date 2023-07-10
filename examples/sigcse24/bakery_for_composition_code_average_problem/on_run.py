from pedal import *
from curriculum_sneks import *

suppress("algorithmic", "iterating_over_empty_list")
suppress("algorithmic", "multiple_return_types")
prevent_advanced_iteration(allow_for=True)

average_def = find_function_definition('average')
if average_def:
    if average_def.find_all("For"):
        gently("You should not be directly looping in `average`",
               title="Loop Indirectly", label="looping_directly")
    if not find_function_calls("count", root=average_def):
        gently("You haven't composed `count`.",
               title="Compose Functions", label="not_composing_count")
    if not find_function_calls("summate", root=average_def):
        gently("You haven't composed `summate`.",
               title="Compose Functions", label="not_composing_summate")


#ins_cont.missing_zero_initialization()
#ins_cont.warning_average_in_iteration()
#ins_cont.wrong_average_denominator()
#ins_cont.wrong_average_numerator()

prevent_printing_functions()
ensure_functions_return()
ensure_function('average', parameters=['[int]'], returns=float)
ensure_function_call('average', at_least=2)
ensure_coverage(.9)
ensure_cisc108_tests(3)
ensure_called_uniquely('average', 3)
unit_test('average',
          ([[1, 2, 3]], 2.0),
          ([[1]], 1.0),
          ([[4, 4, 4]], 4.0),
          ([[0]], 0.0))
