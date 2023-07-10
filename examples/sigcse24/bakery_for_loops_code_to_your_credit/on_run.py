from pedal import *

prevent_ast("While", label="used_while", title="Do Not Use While Loops",
            priority='highest',
            message="Do not use a <code>while</code> loop. This kind of"
                    " loop may be popular in other languages, but it"
                    " has limited use in Python. Also, we're learning about"
                    " for loops.")
ensure_ast("For", at_least=1)
prevent_ast("For", at_most=1)
ensure_ast("List", at_least=1)
prevent_ast("List", at_most=1)
prevent_literal_type(str)
ensure_literal_type(int, at_least=1)

ast = parse_program()
fors = ast.find_all("For")
if fors and any(s.find_all("List") for s in fors[0].body):
    explain("Do not initialize the List inside the `for` loop. That"
            " is problematic, because it re-initializes the list"
            " multiple times!", title="Initializing List in Loop",
            label="list_init_in_loop", priority='highest')

if not find_match("for ___ in ___: print(___)"):
    explain("The <code>print</code> call should be INSIDE the loop.",
            label="print_not_in_loop", title="Print Not In Loop")

assert_not_output_contains(student, '[',
                           label="output_has_bracket", title="Print Elements, Not List",
                           message="You should be printing out individual elements, not the entire list.")

if not get_output():
    gently("You are not printing anything.", label="no_output", title="No Output")
