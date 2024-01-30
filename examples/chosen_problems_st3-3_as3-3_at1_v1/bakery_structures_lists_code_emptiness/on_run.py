from pedal import *

prevent_literal("[]")
ensure_literal([])
ensure_function_call('print')
assert_output(student, "[]")