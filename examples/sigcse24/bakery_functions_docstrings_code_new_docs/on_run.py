from pedal import *
from curriculum_sneks import *

prevent_printing_functions()
ensure_functions_return()

ensure_function('is_expected_user', parameters=[str, int, float], returns=bool)

ast = parse_program()
prevent_ast('FunctionDef', at_most=1)
defs = ast.find_all("FunctionDef")
if defs:
    defs = defs[0]
    for lineno, statement in enumerate(defs.body):
        if (statement.ast_name == "Expr" and
                statement.value.ast_name in ("Constant", "Str")):
            if lineno == 0:
                break
            else:
                gently("The string literal must be the first line of the"
                       " function's body.", label="docstring_not_first_line",
                       title="Incorrect Documentation Location", priority='syntax')
    else:
        gently("You have not provided valid documentation for the function.",
               priority='syntax', label='missing_documentation', title="Missing Documentation")
