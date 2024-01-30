from pedal import *
from curriculum_sneks import *

if "$" in get_program():
    explain("You should not use the dollar sign ($) anywhere in your code!",
            priority='syntax', label="used_dollar_sign", title="Do Not Use Dollar Sign")

if find_match("round('9.5')"):
    explain("You attempted to round the string literal '9.5', but you cannot do that."
            " Remember, you must first convert the string literal to a float using the"
            " float function.",
            priority='syntax', label="rounding_string", title="Rounding String")

ensure_function_call('round')
ensure_function_call('float')
ensure_function_call('print')

prevent_ast("Num")
ensure_literal("9.5")
prevent_literal("'9'")
prevent_ast("Assignment", at_most=1, label="too_many_assignments", title="Too Many Assignments",
            message="You should only need one assignment statement.")

if not assert_output(student, "10"):
    correct_output()

str_vars = student.get_values_by_type(str)
float_vars = student.get_values_by_type(float)+student.get_values_by_type(int)

if not float_vars:
    gently("You need to create a variable with the right value.",
           label="missing_float_variable", title="Missing Variable")
elif float_vars[0] == 10.0:
    guidance("Great! Now, use [Evaluate] to call those functions again - but "
             "remember, do not print! Just call the `round` and `float` functions "
             "with a new value.", label="need_eval", title="Part 2")
elif float_vars[0] == 9.5:
    gently("Your variable has the wrong value. Make sure you round "
           "the value before storing it in the variable!",
           label="not_rounding", title="Not Rounding")
elif str_vars and str_vars[0] in ("9.5", "9.50"):
    gently("Your variable has the wrong value. Make sure you convert "
           "the value to a float before storing it in the variable!",
           label="not_converting_to_float", title="Not Converting to Float")
else:
    gently("Your variable has the wrong value.", label="wrong_result",
           title="Variable Has Wrong Value")
