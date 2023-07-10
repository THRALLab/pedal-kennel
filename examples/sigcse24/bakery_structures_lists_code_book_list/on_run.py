from pedal import *

ensure_ast('List', at_least=1)
prevent_ast('List', at_most=1)

variables = student.get_values_by_type(list)

if not variables:
    gently("You must create a new list variable.", label="no_list_variables",
           title="Missing List Variable")
elif len(variables) > 1:
    gently("Only create one list variable.", label="too_many_list_variables",
           title="Too Many List Variables")
else:
    variables = variables[0]
    if len(variables) < 3:
        gently("You need at least 3 strings in your list variable.",
               label="too_few_strings_in_list", title="List Not Long Enough")
    elif any([not isinstance(v, str) for v in variables]):
        gently("All of the elements in the list must be strings.",
               label="non_string_list", title="List Must Have Strings")
    elif ensure_function_call('print'):
        assert_output(student, repr(variables))