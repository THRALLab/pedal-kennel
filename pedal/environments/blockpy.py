"""
Environment to support BlockPy.

# Support our sysmodules hack by clearing out any lingering old data
from pedal.core.report import MAIN_REPORT
MAIN_REPORT.clear()

# Interface for interacting with BlockPy
from utility import *

from pedal.environments.blockpy import setup_pedal
pedal = setup_pedal(skip_tifa=${skip_tifa},
                    main_file='answer.py',
                    main_code=${safeCode})

# Execute students' code
if not get_model_info('assignment.settings.disableInstructorRun'):
    set_inputs(get_model_info('execution.input'))
    student = run()
else:
    student = get_sandbox()

# Load in some commonly used tools
from pedal.cait.cait_api import parse_program
from pedal.sandbox.commands import *

# TODO: Set up mock coverage tool in BlockPy
# Monkey-patch trace_lines
from pedal.sandbox import commands
commands.trace_lines = trace_lines
# TODO: Refactor resolver to return instructions
# Monkey-patch questions
from pedal import questions
questions.show_question = set_instructions

# Run the actual instructor code
${instructorCode}

# Resolve everything
final = pedal.resolve()
SUCCESS = final.success
SCORE = final.score
CATEGORY = final.category
LABEL = final.title
MESSAGE = final.message
DATA = final.data
HIDE = final.hide_correctness
"""
from pedal.core.environment import Environment
from pedal.core.report import MAIN_REPORT
from pedal.sandbox import Sandbox

def enhance_runtime_errors(feedback):
    line.replace(', in <module>', '', 1)
    pass

class BlockPyEnvironment(Environment):
    """
    Configures the BlockPy programming environment.
    """
    def __init__(self, files=None, main_file='answer.py', main_code=None,
                 user=None, assignment=None, course=None, execution=None,
                 instructor_file='on_run.py', skip_tifa=False, set_success=True,
                 report=MAIN_REPORT):
        super().__init__(files=files, main_file=main_file, main_code=main_code,
                         user=user, assignment=assignment, course=course,
                         execution=execution, instructor_file=instructor_file,
                         report=report)


    def setup_pedal(self):
        student = MAIN_REPORT['sandbox']['run'] = Sandbox(report=self.report)
        student.report_exceptions_mode = True
        commands.run_student(raise_exceptions=False)

setup_pedal = BlockPyEnvironment
