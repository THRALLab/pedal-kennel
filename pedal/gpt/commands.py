import json
import os

from pedal.core.report import MAIN_REPORT
from pedal.gpt.constants import TOOL_NAME
from pedal.gpt.feedbacks import gpt_prompt_feedback

try:
    import openai
except ImportError:
    print("OpenAI library not found!")

__all__ = ['gpt_get_api_key', 'gpt_run_prompts']


def gpt_get_api_key(default):
    """
    Takes a fallback string and returns the API key, or the fallback
    if the environment variable doesn't exist.

    Args:
        default (str): The fallback API key. Probably passed as a CLI arg
    """
    return os.getenv("OPENAI_API_KEY", default=default)


def add_feedback(feedback, report):
    """
    Adds a feedback message.

    Args:
        feedback (str):
        report:
    """
    report[TOOL_NAME]['feedback'].append(gpt_prompt_feedback(feedback))


def gpt_run_prompts(api_key, code=None, report=MAIN_REPORT):
    """
    Evaluates the prompts and attach the results to the Report.

    Args:
        api_key:
        code (str or None): The code to evaluate with TIFA. If ``code`` is not
            given, then it will default to the student's main file.
        report (:class:`pedal.core.report.Report`): The Report object to
            attach results to.
    """
    if not code:
        code = report.submission.main_code

    prompts = [f"""Here is my Python code:
    {code}
    Please identify any problems with it."""]

    feedback = report[TOOL_NAME]['feedback']

    for prompt in prompts:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',  # must add -0613 for functions??
            messages=[{'role': 'user', 'content': prompt}],
            functions=[
                {
                    'name': 'add_feedback',
                    'description': 'Called when there is a problem with the code. ' +
                                   'If there are no problems, do not call the function.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'feedback': {
                                'type': 'string',
                                'description': 'A concise message explaining the problem with the code.'
                            }
                        },
                        'required': ['feedback']
                    }
                }
            ],
            function_call='auto'
        )
        response_message = response['choices'][0]['message']

        if response_message.get('function_call'):
            # todo: handle incorrect responses
            if response_message['function_call']['name'] == 'add_feedback':
                args = json.loads(response_message["function_call"]["arguments"])
                add_feedback(args['feedback'], report)
            else:
                print('Invalid function:', response_message['function_call']['name'])
        else:
            print('Response:', response_message['content'])
