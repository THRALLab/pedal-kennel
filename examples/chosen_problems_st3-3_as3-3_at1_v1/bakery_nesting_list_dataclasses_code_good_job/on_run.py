from pedal import *
from curriculum_sneks import *
from dataclasses import dataclass

prevent_printing_functions()
ensure_functions_return()

prevent_operator("is", message="You do not need the `is` operator.")
prevent_operator("is not", message="You do not need the `is not` operator.")
prevent_operator("==", message="You do not need the `==` operator.")
prevent_operator("!=", message="You do not need the `!=` operator.")

if not find_match('''UNEMPLOYED = Job("Unemployed", 0, True, "None")'''):
    explain("Do not remove or alter the starting code that we gave you. You may need to check your history or reset the problem.")

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str


ensure_dataclass(Job, priority='instructor')
assert_is_instance(evaluate("Job"), type)

ensure_function('best_job', 1, ['list[Job]'], 'Job')
ensure_function_callable('best_job')

ensure_coverage(.9)
ensure_cisc108_tests(2)
ensure_function_call('Job', 2)
ensure_called_uniquely('best_job', 2)

UNEMPLOYED = evaluate('UNEMPLOYED')
with CommandBlock() as context:
    jp_se = call('Job', 'Software Engineer', 125, True, 'JP Morgan', target='jp_se')
    mt_sse = call('Job', 'Senior Software Engineer', 195, False, 'M&T', target='mt_sse')
    google_se = call('Job', 'Software Engineer', 200, True, 'Google', target='google_se')
    colgate_ux = call('Job', 'UX Designer', 135, True, 'Colgate', target='colgate_ux')
    jp_db = call('Job', 'Database Admin', 153, True, 'JP Morgan', target='jp_db')
    bc_ceo = call('Job', 'CEO', 400, False, 'Better Code', target='bc_ceo')

unit_test('best_job', 
          ([[]], UNEMPLOYED),
          ('[jp_se]', jp_se),
          ('[mt_sse, jp_se, google_se]', google_se),
          ('[jp_se, jp_db, colgate_ux]', jp_db),
          ('[mt_sse, bc_ceo]', UNEMPLOYED),
          ('[google_se, jp_db, jp_se, mt_sse, colgate_ux, bc_ceo]', google_se),
          context=context
)

