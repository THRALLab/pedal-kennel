from pedal import *

if "%" in get_program():
    explain("You should not use a % in your code."
            " How do you represent a number like 50% in Python?",
            priority='syntax', label="bad_percent_sign", title="Do Not Use %")

ensure_ast("If", at_least=1)
prevent_ast("If", at_most=1)
ensure_ast("Compare")

m1 = "It will probably rain."
m2 = "It might not rain."
ensure_literal(m1)
ensure_literal(m2)

if (m1 in student.raw_output) == (m2 in student.raw_output):
    gently("You are not printing one of the two possible answers.",
           label="wrong_output", title="Wrong Output")

if not find_match(".5") and not find_match("50"):
    gently("You will need to represent the number 50% as a"
           " float literal value. How should you"
           " represent 50% as a decimal number?",
           label="not_using_decimal_5", title="Missing 50% Value")

assert_has_variable(student, 'precipitation')
#console_debug(evaluate('precipitation'))
if not isinstance(student.data.get('precipitation'), float):
    gently("The precipitation is not a float value.",
          label="precipitation_is_not_float", title="Variable Has Wrong Type")
#assert_type(evaluate('precipitation'), float)
