import argparse
import json
import os
from configparser import ConfigParser
from dataclasses import dataclass

from pedal import MAIN_REPORT
from pedal.command_line.modes import AbstractPipeline
from pedal.core.feedback_category import FeedbackCategory
from pedal.gpt.constants import TOOL_NAME as GPT_TOOL_NAME

arg_parser = argparse.ArgumentParser(description='Run student code through Pedal and store the feedback.')
arg_parser.add_argument('-m', '--max_submissions', type=int, action='store', default=6)
arg_parser.add_argument('-i', '--instructor', type=str, action='store', default='Instructor')

args = arg_parser.parse_args()


@dataclass
class SubmissionBlock:
    # student = ''  # isn't this covered by the filename?
    student_code = ''
    gpt_feedback = ''
    gpt_feedback_length = ''
    # gpt_feedback_word_probability = -1
    gpt_error_type = ''
    gpt_score = -1
    pedal_feedback = ''
    pedal_feedback_length = -1
    # pedal_feedback_word_probability = -1
    pedal_score = -1
    rubric_fields = None
    instructor_feedback = None

    def add_to_output(self, assignment: str, filename: str, cfg: ConfigParser) -> None:
        cfg[f'{assignment}.{filename}'] = {
            'student_code':          self.student_code,
            'gpt_feedback':          self.gpt_feedback,
            'gpt_feedback_length':   self.gpt_feedback_length,
            'gpt_error_type':        self.gpt_error_type,
            'gpt_score':             self.gpt_score,
            'pedal_feedback':        self.pedal_feedback,
            'pedal_feedback_length': self.pedal_feedback_length,
            'pedal_score':           self.pedal_score,
            'rubric_fields':         self.rubric_fields,
            'instructor_feedback':   self.instructor_feedback
        }


@dataclass
class AssignmentBlock:
    assignment = ''  # directory
    description = ''  # index.md
    student_submissions = {}

    def add_submission(self, filename: str, submission: SubmissionBlock):
        self.student_submissions[filename] = submission

    def add_to_output(self, cfg) -> None:
        cfg[self.assignment] = {
            'description': self.description
        }
        for filename, submission in self.student_submissions.items():
            submission.add_to_output(self.assignment, filename, cfg)


class SubmissionPipeline(AbstractPipeline):
    def __init__(self, current_submission: SubmissionBlock, config):
        super().__init__(config)
        self.current_submission = current_submission
        with open(self.config.submissions) as student_code:
            self.current_submission.student_code = '\n' + student_code.read().strip()

    def run_control_scripts(self):
        self.submissions[0].script += '\nfrom pedal.gpt import gpt_run_prompts\ngpt_run_prompts()'
        for bundle in self.submissions:
            bundle.run_ics_bundle(resolver=self.config.resolver,
                                  skip_tifa=self.config.skip_tifa,
                                  skip_run=self.config.skip_run)
            bundle.result.feedback = list(MAIN_REPORT.feedback)

    def process_output(self):
        if len(self.submissions) == 0:
            return  # should never happen

        found_feedback = False
        found_gpt_feedback = False
        for bundle in self.submissions:
            if len(bundle.result.resolution.used) == 0:
                continue
            for feedback in bundle.result.feedback:
                if not found_feedback and feedback.category != FeedbackCategory.PATTERNS:
                    self.current_submission.pedal_feedback = feedback.message.strip()
                    self.current_submission.pedal_feedback_length = len(
                        self.current_submission.pedal_feedback.split(' '))
                    self.current_submission.pedal_score = bundle.result.resolution.score
                    found_feedback = True
                if not found_gpt_feedback and feedback.category == FeedbackCategory.PATTERNS:
                    self.current_submission.gpt_feedback = feedback.message.strip()
                    self.current_submission.gpt_feedback_length = len(self.current_submission.gpt_feedback.split(' '))
                    # self.current_submission.gpt_error_type = bundle.result.resolution
                    self.current_submission.gpt_score = feedback.score
                    found_gpt_feedback = True
                if found_feedback and found_gpt_feedback:
                    break
            if not found_feedback or not found_gpt_feedback:
                print(
                    f"  - Didn't find feedback! Feedbacks: {[feedback.category for feedback in bundle.result.feedback]}")


# read in all student programs
num_submissions_processed = 0
assignments = []

for directory in os.listdir(os.getcwd()):
    if not os.path.isdir(directory):
        continue

    assignment = AssignmentBlock()
    assignment.assignment = directory
    with open(f'{directory}/index.md') as description:
        assignment.description = description.read().strip()

    print(f'Processing assignment {directory}')

    path = f'{directory}/submissions/'
    for file in os.listdir(path):
        filepath = path + file
        if not file.endswith('.py') or os.stat(filepath).st_size == 0:
            continue

        num_submissions_processed += 1
        if 0 < args.max_submissions < num_submissions_processed:
            break

        print(f'- Processing submission {file}')

        submission = SubmissionBlock()

        pipeline = SubmissionPipeline(submission, {
            'instructor': f'{directory}/on_run.py',
            'submissions': filepath,
            'environment': 'blockpy',
            'resolver': 'resolve',
            'skip_tifa': False,
            'skip_run': False,
            'threaded': False,
            'alternate_filenames': False,
            'ics_direct': False
        })
        pipeline.execute()

        assignment.add_submission(file, submission)

    assignments.append(assignment)

    if 0 < args.max_submissions < num_submissions_processed:
        break

# write results to file
with open('feedback_results.ini', 'w') as out_file:
    prompt = json.dumps(MAIN_REPORT[GPT_TOOL_NAME]['prompts_getter']('{{STUDENT_CODE_HERE}}'), indent=2, default=str)

    out = ConfigParser(allow_no_value=True, interpolation=None)
    out['global'] = {
        'instructor': args.instructor,
        'tester': os.getlogin(),
        'gpt_model': MAIN_REPORT[GPT_TOOL_NAME]['model'],
        'gpt_prompt': prompt,
        'gpt_prompt_approximate_length': len(prompt.split(' '))
    }

    for assignment in assignments:
        assignment.add_to_output(out)

    out.write(out_file)
    print('Results written to file!')
