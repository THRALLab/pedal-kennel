import configparser
import os
from dataclasses import dataclass

from pedal.command_line.modes import AbstractPipeline


@dataclass
class CodeFeedback:
    filename = ''
    # student = ''
    # assignment = ''
    # tester = ''  # ???
    # gpt_prompt = ''
    # gpt_prompt_length = 0
    # gpt_feedback = ''
    # gpt_feedback_length = ''
    # gpt_feedback_word_probability = 1.0  # ???
    # gpt_score = 0
    # gpt_error_type = ''  # ???
    # gpt_version = ''
    pedal_feedback = ''
    # pedal_feedback_length = 0  # ???
    # pedal_feedback_word_probability = 1.0  # ???
    # pedal_score = 0
    # rubric_fields = {}  # todo
    # instructor_feedback = {}  # todo

    def add_to_output(self, cfg: configparser.ConfigParser) -> None:
        cfg[self.filename] = self.__dict__
        cfg[self.filename].pop('filename')  # this is the name of the table


student_codes = []


class BakerySubmissionsPipeline(AbstractPipeline):
    def process_output(self):
        for bundle in self.submissions:
            code_feedback = CodeFeedback()
            code_feedback.filename = bundle.submission.main_file
            code_feedback.pedal_feedback = str(bundle.result.resolution)
            student_codes.append(code_feedback)


subset = 100
cwd = os.getcwd()
code_paths = []

# read in all student programs
for directory in os.listdir(cwd):
    if not os.path.isdir(directory):
        continue
    if subset < 0:
        break

    path = f'{directory}/submissions/'
    for file in os.listdir(path):
        filepath = path + file
        if not file.endswith('.py') or os.stat(filepath).st_size == 0:
            continue
        code_paths.append(filepath)
        subset -= 1

for code_path in code_paths:
    # todo: add gpt pipeline when done (my poor api limit)
    pipeline = BakerySubmissionsPipeline({
        'instructor': 'instructor.py',
        'submissions': code_path,
        'environment': 'blockpy',
        'resolver': 'resolve',
        'skip_tifa': False,
        'skip_run': False,
        'threaded': False,
        'alternate_filenames': False,
        'ics_direct': False
    })
    pipeline.execute()

with open('prompt_feedback_results.ini', 'w') as out_file, \
        open('instructor.py') as instructor_code, \
        open('instructor_gpt.py') as instructor_gpt_code:
    out = configparser.ConfigParser(allow_no_value=True)
    out['global'] = {
        'instructor_code': '\n' + instructor_code.read().strip(),
        'instructor_gpt_code': '\n' + instructor_gpt_code.read().strip()
    }

    for feedback in student_codes:
        feedback.add_to_output(out)

    out.write(out_file)
