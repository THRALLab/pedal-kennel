from pedal import *
from curriculum_sneks import *
from curriculum_sneks.tests import *

prevent_printing_functions()
ensure_functions_return()

ensure_function('cut_day', parameters=[str], returns=str)
ensure_coverage(.9)
ensure_cisc108_tests(1)
unit_test('cut_day',
          (['saturday'], 'satur'),
          (['monday'], 'mon'),
          (['Wednesday'], 'Wednes'))
