import argparse
import json
import math
import os
import sys
from configparser import ConfigParser
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from itertools import product
from unittest.mock import patch

from pedal import MAIN_REPORT, Submission
from pedal.command_line.modes import AbstractPipeline, BundleResult, get_python_files, Bundle
from pedal.core.feedback_category import FeedbackCategory
from pedal.gpt.constants import TOOL_NAME as GPT_TOOL_NAME
from pedal.gpt import gpt_run_prompts
from pedal.gpt.feedbacks import gpt_prompt_feedback
from pedal.utilities.files import find_possible_filenames, normalize_path

arg_parser = argparse.ArgumentParser(description='Run student code through Pedal and store the feedback.')
arg_parser.add_argument('-i', '--instructor', type=str, action='store', default='Instructor')

args = arg_parser.parse_args()


@dataclass
class SubmissionBlock:
    # student = ''  # isn't this covered by the filename?
    student_code = ''
    gpt_feedback = ''
    gpt_feedback_length = ''
    # gpt_feedback_word_probability = -1
    # gpt_error_type = ''
    gpt_score = -1
    pedal_feedback = ''
    pedal_feedback_length = -1
    # pedal_feedback_word_probability = -1
    pedal_score = -1

    def add_to_output(self, assignment: str, filename: str, cfg: ConfigParser) -> None:
        section = f'{assignment}.{filename}'
        cfg[section] = {
            'student_code':          self.student_code,
            'gpt_feedback':          self.gpt_feedback,
            'gpt_feedback_length':   self.gpt_feedback_length,
            # 'gpt_error_type':        self.gpt_error_type,
            'gpt_score':             self.gpt_score,
            'pedal_feedback':        self.pedal_feedback,
            'pedal_feedback_length': self.pedal_feedback_length,
            'pedal_score':           self.pedal_score,
        }
        categories = ['accurate', 'concise', 'clear', 'jargon', 'sentiment']
        for key in categories:
            cfg.set(section, f'instructor_feedback_gpt_{key}', '')
        for key in categories:
            cfg.set(section, f'instructor_feedback_pedal_{key}', '')


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


def get_prompts_getter(question_md, temp, top_p):  # yes I know this is horrible
    def get_default_prompts(code=None, report=MAIN_REPORT):
        """
        Returns each prompt to run, as well as the processing function that generates feedback
        from the results. If there is an error at any point, the processing function is never called.

        Args:
            code (str or None): The student's code to evaluate. If ``code`` is not
                given, then it will default to the student's main file.
            report (:class:`pedal.core.report.Report`): The Report object to
                attach results to.
        """
        messages = [
            {
                'role': 'system',
                'content': "You are an intelligent tutor for a introductory computer science course in Python. " +
                           "You never give answers but do give helpful tips to guide students with their code."
            },
            {
                'role': 'assistant',
                'content': f'The student was given this programming problem:\n{question_md}'
            },
            {
                'role': 'user',
                'content': code
            }
        ]
        feedback_function = {
            'name': 'add_code_feedback',
            'description': 'Adds feedback on the code for the student to view.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'feedback': {
                        'type': 'string',
                        'description': 'Helpful tips to guide a student with their problematic code.'
                    },
                    'is_error_present': {
                        'type': 'boolean',
                        'description': 'If there is a problem with the code, this parameter is true.'
                    }
                },
                'required': ['feedback', 'is_error_present']
            }
        }

        prompts = {
            'feedback': (messages, feedback_function, temp, top_p)
        }

        def process_prompts(results):
            gpt_prompt_feedback({
                'feedback': results['feedback']['feedback'],
                'score': 0.0
            })

        return prompts, process_prompts

    return get_default_prompts


class SubmissionBundle(Bundle):
    def __init__(self, config, script, submission, question_md, gpt_model, temp, top_p):
        super().__init__(config, script, submission)
        self.gpt_feedback = None
        self.question_md = question_md
        self.gpt_model = gpt_model
        self.temp = temp
        self.top_p = top_p

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
                    if 'MAIN_REPORT' in global_data:
                        global_data['MAIN_REPORT'][GPT_TOOL_NAME]['model'] = self.gpt_model
                        global_data['MAIN_REPORT'][GPT_TOOL_NAME]['prompts_getter'] = get_prompts_getter(self.question_md, self.temp, self.top_p)
                        gpt_run_prompts()
                    else:
                        print('ERROR! No main report object found!')

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
    def __init__(self, question_md, gpt_model, temp, top_p, current_submission: SubmissionBlock, config):
        super().__init__(config)
        self.question_md = question_md
        self.gpt_model = gpt_model
        self.temp = temp
        self.top_p = top_p
        self.current_submission = current_submission
        with open(self.config.submissions, encoding='utf-8') as student_code:
            self.current_submission.student_code = '\n' + student_code.read().strip()

    def load_file_submissions(self, scripts):
        # Get instructor control scripts
        all_scripts = []
        for script in scripts:
            script_file_name, script_file_extension = os.path.splitext(script)
            # Single Python file
            if script_file_extension in ('.py',):
                with open(script, encoding='utf-8') as scripts_file:
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
                    self.submissions.append(SubmissionBundle(self.config, scripts_contents, new_submission, self.question_md, self.gpt_model, self.temp, self.top_p))
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
                    with open(possible, encoding='utf-8') as single_submission_file:
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
                self.submissions.append(SubmissionBundle(self.config, scripts_contents, new_submission, self.question_md, self.gpt_model, self.temp, self.top_p))
            return load_error

    def run_control_scripts(self):
        for bundle in self.submissions:
            bundle.run_ics_bundle(
                resolver=self.config.resolver,
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
assignments = []
script_parent_dir = os.path.dirname(os.path.realpath(__file__))

gpt_models = ['gpt-4-0613']
temps = [0.0, 1.0, 2.0]
top_ps = [0.0, 1.0]
directories = [entry for entry in os.listdir(script_parent_dir) if not entry.startswith('_') and not entry.endswith('.py')]
trials = 3

num_assignments_total = len(gpt_models) * len(temps) * len(top_ps) * len(directories) * trials
assignments_processed = 0

parameters = product(gpt_models, temps, top_ps, list(range(trials)))
for gpt_model, temp, top_p, trial in parameters:
    if math.floor(temp) == 2 and math.floor(top_p) == 1:
        assignments_processed += 1
        print(f'Skipping invalid combo... ({assignments_processed} / {num_assignments_total})')
        continue  # already collected this data

    for directory in directories:
        assignment = AssignmentBlock()
        assignment.assignment = directory
        with open(f'{script_parent_dir}/{directory}/index.md', encoding='utf-8') as description:
            assignment.description = description.read().strip()

        assignments_processed += 1
        print(f'Processing assignment {directory} ({assignments_processed} / {num_assignments_total})')

        path = f'{script_parent_dir}/{directory}/submissions/'
        for file in os.listdir(path):
            filepath = path + file
            if file.startswith('bakery') or not file.endswith('.py') or os.stat(filepath).st_size == 0:
                continue

            print(f'- Processing submission {file}')

            submission = SubmissionBlock()

            pipeline = SubmissionPipeline(assignment.description, gpt_model, temp, top_p, submission, {
                'instructor': f'{script_parent_dir}/{directory}/on_run.py',
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

    # write results to file
    with open(f'{script_parent_dir}/_feedback_results/{gpt_model}-temp-{temp}-top_p-{top_p}-{trial}.ini', 'w', encoding='utf-8') as out_file:
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
