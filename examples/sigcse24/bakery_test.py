import argparse
import os
from configparser import ConfigParser
from dataclasses import dataclass

from pedal.command_line.modes import AbstractPipeline
from pedal.core.feedback_category import FeedbackCategory

arg_parser = argparse.ArgumentParser(description='Run student code through Pedal and store the feedback.')
arg_parser.add_argument('-m', '--max_submissions', type=int, action='store', default=1)
arg_parser.add_argument('-i', '--instructor', type=str, action='store', default='Instructor')

args = arg_parser.parse_args()


@dataclass
class SubmissionBlock:
    # student = ''  # @acbart
    # gpt_prompt = ''
    # gpt_prompt_length = -1
    gpt_feedback = ''
    gpt_feedback_length = ''
    # gpt_feedback_word_probability = -1  # ???
    gpt_score = -1
    # gpt_error_type = ''  # ???
    # gpt_version = ''
    pedal_feedback = ''
    pedal_feedback_length = -1  # word count
    # pedal_feedback_word_probability = -1
    pedal_score = -1
    rubric_fields = None
    instructor_feedback = None

    def add_to_output(self, assignment: str, filename: str, cfg: ConfigParser) -> None:
        cfg[f'{assignment}.{filename}'] = {
            'gpt_feedback':          self.gpt_feedback,
            'gpt_feedback_length':   self.gpt_feedback_length,
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

    def process_output(self):
        if len(self.submissions) == 0:
            return  # should never happen

        found_feedback = False
        found_gpt_feedback = False
        for bundle in self.submissions:
            if not found_feedback and bundle.result.resolution.category != FeedbackCategory.PATTERNS:
                self.current_submission.pedal_feedback = bundle.result.output.strip()
                self.current_submission.pedal_feedback_length = len(bundle.result.resolution.message.strip().split(' '))
                self.current_submission.pedal_score = bundle.result.resolution.score
                found_feedback = True
            if not found_gpt_feedback and bundle.result.resolution.category == FeedbackCategory.PATTERNS:
                self.current_submission.gpt_feedback = bundle.result.resolution.message.strip()
                self.current_submission.gpt_feedback_length = len(self.current_submission.gpt_feedback.split(' '))
                self.current_submission.gpt_score = bundle.result.resolution.score
                found_gpt_feedback = True
            if found_feedback and found_gpt_feedback:
                break


# read in all student programs
num_submissions_processed = 0
assignments = []

for directory in os.listdir(os.getcwd()):
    if not os.path.isdir(directory):
        continue

    if num_submissions_processed > args.max_submissions:
        break

    assignment = AssignmentBlock()
    assignment.assignment = directory
    with open(f'{directory}/index.md') as description:
        assignment.description = description.read().strip()

    path = f'{directory}/submissions/'
    for file in os.listdir(path):
        filepath = path + file
        if not file.endswith('.py') or os.stat(filepath).st_size == 0:
            continue

        num_submissions_processed += 1
        if num_submissions_processed > args.max_submissions:
            break

        submission = SubmissionBlock()

        pipeline_settings = {
            'instructor': 'instructor.py',
            'submissions': path,
            'environment': 'blockpy',
            'resolver': 'resolve',
            'skip_tifa': False,
            'skip_run': False,
            'threaded': False,
            'alternate_filenames': False,
            'ics_direct': False
        }

        pipeline = SubmissionPipeline(submission, pipeline_settings)
        pipeline.execute()

        assignment.add_submission(file, submission)

    assignments.append(assignment)

# write results to file
with open('feedback_results.ini', 'w') as out_file:
    out = ConfigParser(allow_no_value=True, interpolation=None)
    out['global'] = {
        'instructor': args.instructor,
        'tester': os.getlogin()
    }

    for assignment in assignments:
        assignment.add_to_output(out)

    out.write(out_file)
