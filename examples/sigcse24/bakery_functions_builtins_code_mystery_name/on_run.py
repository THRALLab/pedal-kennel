from pedal import *

ensure_starting_code('''message = "Why are you shouting?"''')
prevent_embedded_answer('''"WHY ARE YOU SHOUTING?"''')

if not find_function_calls('upper'):
    explain(label="missing_upper", title="Missing Function",
            message="What is the name of the method that converts a"
                    " string to uppercase? Double check the documentation!")
if "Why are you shouting?" in get_output():
    gently("You are printing the string unmodified. It needs to be all upper case.",
           label="not_uppercasing", title="Not Printing Uppercase")

assert_output(student, "WHY ARE YOU SHOUTING?")
