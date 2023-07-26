from pedal import *
from curriculum_sneks import ensure_functions_return, prevent_printing_functions
from curriculum_sneks.tests import ensure_cisc108_tests

prevent_printing_functions()
ensure_functions_return()

ensure_function('is_morning', parameters=[int], returns=bool)
ensure_function_call('is_morning', at_least=3)
for helper_name in ['is_past_dawn', 'is_before_noon']:
    ensure_function(helper_name, parameters=[int], returns=bool)
    ensure_function_call(helper_name, at_least=1)
    prevent_function_call(helper_name, at_most=1)
ensure_coverage(.9)
ensure_cisc108_tests(4)
ensure_called_uniquely('is_morning', 4)
unit_test("is_morning",
          ([1], False),
          ([5], True),
          ([6], True),
          ([9], True),
          ([12], True),
          ([16], False))

if unit_test("is_past_dawn",
             ([1], False),
             ([5], True),
             ([6], True)):
    compliment("is_past_dawn is correct", label="done_is_past_dawn")

if unit_test("is_before_noon",
             ([1], True),
             ([11], True),
             ([13], False)):
    compliment("is_before_noon is correct", label="done_is_before_noon")

is_morning = find_function_definition('is_morning')

if not find_function_calls('is_past_dawn', root=is_morning):
    gently("You need to use `is_past_dawn` inside of `is_morning`.",
           label="not_using_is_past_dawn", title="Not Using is_past_dawn")
if not find_function_calls('is_before_noon', is_morning):
    gently("You need to use `is_before_noon` inside of `is_morning`.",
           label="not_using_is_before_noon", title="Not Using is_before_noon")
