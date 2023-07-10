from pedal import *

if ''''The dog's house is big and red.''' in get_program():
    explain("You attempted to put single quotes around a string that already "
            "had single quotes. You should use double quotes on the outside!",
            priority='syntax', label="doubled_single_quotes",
            title="Double Single Quotes")

ensure_function_call('print')


if "The dog's house is big and red." not in get_output():
    if 'The dog"s house is big and red.' in get_output():
        gently("You should be using single, not double, quotes!",
               label="abused_double_quotes", title="Double Not Single")
    elif get_output():
        if '"' in get_output()[0]:
            gently("You should not be printing any double quotes.",
                   label="printing_double_quotes", title="No Double Quotes")
        else:
            gently("You are printing the wrong string.",
                   label="wrong_output", title="Wrong Output")
    else:
        gently("You have not printed anything!", label="no_output", title="No Output")
