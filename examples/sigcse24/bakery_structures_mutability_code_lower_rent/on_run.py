from pedal import *

message = "THE RENT IS TOO HIGH!"

ensure_literal(message)
prevent_literal(message.lower())
assert_has_variable(student, 'message')
evaluated_message = evaluate('message')
assert_equal(evaluated_message, message.lower(),
             message="You have not made the variable's value lowercase; it is still all caps.",
            exact_strings=True)
