from pedal import *

ensure_import('my_second_module')
prevent_literal_type(str)

if 'my_second_module.py' in get_program():
    explain("You should not have the `.py` part of the filename in your `import` statement. Only use the name of the module on its own!")

if 'my_second_module' in student.data:
    answer = student.data['my_second_module'].art
    prevent_literal(answer)
    assert_output(student, answer)
elif 'art' in student.data:
    answer = student.data['art']
    prevent_literal(answer)
    assert_output(student, answer)
else:
    gently("You have not yet imported the `art` variable from the module!")