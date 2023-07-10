from pedal import *
from curriculum_sneks import *
from dataclasses import dataclass

prevent_printing_functions()
ensure_functions_return()

@dataclass
class Turtle:
    speed: int
    direction: int

ensure_dataclass(Turtle, priority='instructor')
assert_is_instance(evaluate("Turtle"), type)

ensure_function('point_turtle', 2, ['Turtle', int], 'Turtle')
ensure_function_callable('point_turtle')

ensure_coverage(.9)
ensure_cisc108_tests(2)
ensure_function_call('Turtle', 2)
ensure_called_uniquely('point_turtle', 2)

unit_test('point_turtle', 
          ([call('Turtle', 5, 90), 0], call('Turtle', 5, 0)),
          ([call('Turtle', 8, 90), 45], call('Turtle', 8, 45)),
          ([call('Turtle', 0, 0), 90], call('Turtle', 0, 90)),
)
