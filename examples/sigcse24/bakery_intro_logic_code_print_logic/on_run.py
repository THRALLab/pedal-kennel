from pedal import *

ensure_function_call('print', at_least=3)
prevent_function_call('print', at_most=3)

output_msg = "Don't just print the word True or False! Instead, write a condition that will evaluate to those values."

prevent_literal(True, message=output_msg)
prevent_literal(False, message=output_msg)
prevent_literal("True", message=output_msg)
prevent_literal("False", message=output_msg)

ensure_literal_type(int)
ensure_literal_type(int)
ensure_literal_type(int)

ensure_literal(8)
ensure_operation(">", message="Does your first statement include the correct operation for 'greater than'?")
ensure_operation("and", message="For your second statement, make sure to include two conditions statements combined with 'and'!")
ensure_literal(7)

ensure_literal(60, at_least=2)
prevent_literal(60, at_most=2)
ensure_operation("<", at_least=2, message="Does your second statement include the correct operation for 'less than' both times?")
prevent_operation(">", at_most=2)
ensure_literal(100, at_least=1)
prevent_literal(100, at_most=1)
ensure_literal(50, at_least=1)
prevent_literal(50, at_most=1)

ensure_literal(2022)
ensure_operation("!=", message="Does your final statement include the correct operation for 'not equal to'?")
ensure_literal(2015)

assert_output(student, "True\nFalse\nTrue")