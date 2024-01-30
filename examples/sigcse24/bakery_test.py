import argparse
import json
import os
import sys
from configparser import ConfigParser
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from unittest.mock import patch

from pedal import MAIN_REPORT, Submission
from pedal.command_line.modes import AbstractPipeline, BundleResult, get_python_files, Bundle
from pedal.core.feedback_category import FeedbackCategory
from pedal.gpt.constants import TOOL_NAME as GPT_TOOL_NAME
from pedal.utilities.files import find_possible_filenames, normalize_path

arg_parser = argparse.ArgumentParser(description='Run student code through Pedal and store the feedback.')
arg_parser.add_argument('-m', '--max_submissions', type=int, action='store', default=0)
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
    student_submissions = None

    def __init__(self):
        if self.student_submissions is None:
            self.student_submissions = {}

    def add_submission(self, filename: str, submission: SubmissionBlock):
        self.student_submissions[filename] = submission

    def add_to_output(self, cfg) -> None:
        cfg[self.assignment] = {
            'description': self.description
        }
        for filename, submission in self.student_submissions.items():
            submission.add_to_output(self.assignment, filename, cfg)


class SubmissionBundle(Bundle):
    def __init__(self, config, script, submission):
        super().__init__(config, script, submission)
        self.gpt_feedback = None

    def run_ics_bundle(self, resolver='resolve', skip_tifa=False, skip_run=False):
        """
        Runs the given instructor control script on the given submission, with the
        accompany contextualizations.
        """
        ics_args = [self.submission, self.environment]
        captured_output = StringIO()
        global_data = {}
        error = None
        resolution = None
        if self.environment:
            env = __import__('pedal.environments.' + self.environment,
                             fromlist=[''])
            global_data.update(env.setup_environment(self.submission,
                                                     skip_tifa=skip_tifa,
                                                     skip_run=skip_run,
                                                     threaded=self.config.threaded).fields)
        else:
            MAIN_REPORT.contextualize(self.submission)
        with redirect_stdout(captured_output):
            with patch.object(sys, 'argv', ics_args):
                try:
                    grader_exec = compile(self.script,
                                          self.submission.instructor_file, 'exec')
                    exec(grader_exec, global_data)

                    for feedback in MAIN_REPORT.feedback:
                        if feedback.category == FeedbackCategory.PATTERNS:
                            self.gpt_feedback = feedback
                            MAIN_REPORT.feedback.remove(feedback)
                            break

                    if 'MAIN_REPORT' in global_data:
                        if not global_data['MAIN_REPORT'].resolves:
                            if resolver in global_data:
                                resolution = global_data[resolver]()
                            # TODO: Need more elegance/configurability here
                            elif self.config.resolver == 'resolve':
                                exec("from pedal.resolvers import print_resolve", global_data)
                                resolution = global_data["print_resolve"]()
                        else:
                            resolution = global_data['MAIN_REPORT'].resolves[-1]
                except Exception as e:
                    error = e
        actual_output = captured_output.getvalue()
        self.result = BundleResult(global_data, actual_output, error, resolution)


class SubmissionPipeline(AbstractPipeline):
    def __init__(self, current_submission: SubmissionBlock, config):
        super().__init__(config)
        self.current_submission = current_submission
        with open(self.config.submissions) as student_code:
            self.current_submission.student_code = '\n' + student_code.read().strip()

    def load_file_submissions(self, scripts):
        # Get instructor control scripts
        all_scripts = []
        for script in scripts:
            script_file_name, script_file_extension = os.path.splitext(script)
            # Single Python file
            if script_file_extension in ('.py',):
                with open(script, 'r') as scripts_file:
                    scripts_contents = scripts_file.read()
                all_scripts.append((script, scripts_contents))
        given_submissions = self.config.submissions
        # If submission is a directory, use it as a directory adjacent to each ics
        if os.path.isdir(given_submissions):
            for script, scripts_contents in all_scripts:
                directory_pattern = given_submissions
                submission_dir = normalize_path(directory_pattern, script)
                submission_files = [
                    os.path.join(submission_dir, sub)
                    for sub in os.listdir(submission_dir)
                ]
                subs = get_python_files(submission_files)
                for main_file, main_code in subs.items():
                    new_submission = Submission(
                        main_file=main_file, main_code=main_code,
                        instructor_file=script
                    )
                    self.submissions.append(SubmissionBundle(self.config, scripts_contents, new_submission))
        # Otherwise, if the submission is a single file:
        # Maybe it's a Progsnap DB file?
        elif given_submissions.endswith('.db'):
            for script, scripts_contents in all_scripts:
                self.load_progsnap(given_submissions, instructor_code=scripts_contents)
        # Otherwise, must just be a single python file.
        else:
            main_file = given_submissions
            load_error, possible_load_error = None, None
            alternatives = [given_submissions]
            # if alternative filenames given, we'll queue them up
            if self.config.alternate_filenames:
                alternatives.extend(find_possible_filenames(self.config.alternate_filenames))
            # Run through all possible filenames
            for possible in alternatives:
                try:
                    with open(possible, 'r') as single_submission_file:
                        main_code = single_submission_file.read()
                        main_file = possible
                    break
                except OSError as e:
                    # Only capture the first possible load error
                    if possible_load_error is None:
                        possible_load_error = e
            else:
                # Okay, file does not exist. Load error gets triggered.
                main_code = None
                load_error = possible_load_error
            for script, scripts_contents in all_scripts:
                new_submission = Submission(
                    main_file=main_file, main_code=main_code,
                    instructor_file=script, load_error=load_error
                )
                self.submissions.append(SubmissionBundle(self.config, scripts_contents, new_submission))
            return load_error

    def run_control_scripts(self):
        for bundle in self.submissions:
            bundle.script += '\nfrom pedal.gpt import gpt_run_prompts\ngpt_run_prompts()'
            bundle.run_ics_bundle(resolver=self.config.resolver,
                                  skip_tifa=self.config.skip_tifa,
                                  skip_run=self.config.skip_run)

    def process_output(self):
        if len(self.submissions) != 1:
            return  # should never happen

        bundle = self.submissions[0]

        if bundle.result.resolution:
            self.current_submission.pedal_feedback = bundle.result.resolution.message.strip()
            self.current_submission.pedal_feedback_length = len(self.current_submission.pedal_feedback.split(' '))
            self.current_submission.pedal_score = bundle.result.resolution.score

        if bundle.gpt_feedback:
            self.current_submission.gpt_feedback = bundle.gpt_feedback.message.strip()
            self.current_submission.gpt_feedback_length = len(self.current_submission.gpt_feedback.split(' '))
            # self.current_submission.gpt_error_type = bundle.result.resolution
            self.current_submission.gpt_score = bundle.gpt_feedback.score
        else:
            print('No GPT response for this submission!')


# read in all student programs
num_submissions_processed = 0
assignments = []
script_parent_dir = os.path.dirname(os.path.realpath(__file__))

for directory in os.listdir(script_parent_dir):
    if not os.path.isdir(directory) or not directory.startswith('bakery'):
        continue

    assignment = AssignmentBlock()
    assignment.assignment = directory
    with open(f'{directory}/index.md') as description:
        assignment.description = description.read().strip()

    print(f'Processing assignment {directory}')

    path = f'{script_parent_dir}/{directory}/submissions/'
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

    out = ConfigParser(allow_no_value=True, interpolation=None, comment_prefixes=(';',))
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
