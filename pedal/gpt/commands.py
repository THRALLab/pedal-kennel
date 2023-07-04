import json
import os

from pedal import system_error
from pedal.core.report import MAIN_REPORT
from pedal.gpt.constants import TOOL_NAME
from pedal.gpt.feedbacks import gpt_prompt_feedback

try:
    import openai
except ImportError:
    openai = None

__all__ = ['gpt_get_api_key', 'gpt_run_prompts']

OPENAI_DEFAULT_MODEL = 'gpt-3.5-turbo-0613'  # 'gpt-4-0613'
OPENAI_RETRY_COUNT = 3


def gpt_get_api_key(default):
    """
    Takes a fallback string and returns the API key, or the fallback
    if the environment variable doesn't exist.

    Args:
        default (str): The fallback API key. Probably passed as a CLI arg
    """
    return os.getenv("OPENAI_API_KEY", default=default)


def run_prompt(model, messages, function, temperature=0.5, top_p=0.5):
    """
    Runs a prompt through OpenAI's api which calls a function, and parses the result.

    Args:
        model: The gpt model to use
        messages: A list of messages to pass to the OpenAI api call
        function: The function to pass to the OpenAI api call
        temperature:
        top_p:
    Returns: A dictionary containing the values of the required arguments, or None if an error is encountered.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=[function],
        function_call={'name': function['name']},
        temperature=temperature,
        top_p=top_p
    )

    if len(response.choices) == 0 or 'function_call' not in response.choices[0]['message']:
        return None
    try:
        args = json.loads(response.choices[0]['message']['function_call']['arguments'])
        for expected_arg in function['parameters']['required']:
            if expected_arg not in args:
                return None
        return args
    except json.JSONDecodeError:
        return None


def gpt_run_prompts(api_key, code=None, model=OPENAI_DEFAULT_MODEL, report=MAIN_REPORT):
    """
    Evaluates the following prompts and attach the results to the Report.

    Args:
        api_key (str): The OpenAI api key
        code (str or None): The student's code to evaluate. If ``code`` is not
            given, then it will default to the student's main file.
        report (:class:`pedal.core.report.Report`): The Report object to
            attach results to.
        model (str): The gpt model to use
    """
    if not openai:
        system_error(TOOL_NAME, 'Could not load OpenAI library!', report=report)
        return
    openai.api_key = api_key

    if not code:
        code = report.submission.main_code

    prompt = f"""{code}"""

    messages = [
        {
            'role': 'system',
            'content': "You are an intelligent tutor for a introductory computer science course in Python. " +
                       "You never give answers but do give helpful tips guide students with their code."
        },
        {
            'role': 'user',
            'content': prompt
        }
    ]

    feedback_result = None
    tries = 0
    while not feedback_result:
        tries += 1
        if tries > OPENAI_RETRY_COUNT:
            system_error(TOOL_NAME, 'Failed to retrieve valid response from OpenAI!', report=report)
            return

        feedback_result = run_prompt(
            model=model,
            messages=messages,
            function={
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
            },
            temperature=0.7)

    score_result = None
    tries = 0
    while not score_result:
        tries += 1
        if tries > OPENAI_RETRY_COUNT:
            system_error(TOOL_NAME, 'Failed to retrieve valid response from OpenAI!', report=report)
            return

        score_result = run_prompt(
            model=model,
            messages=messages,
            function={
                'name': 'add_code_feedback',
                'description': 'Adds feedback on the code for the student to view.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'score': {
                            'type': 'string',
                            'description': 'On a scale from 0 to 10, what would you score their code?'
                        },
                        'error': {
                            'type': 'string',
                            'description': 'List all the error types the code produces.'
                        }
                    },
                    'required': ['score', 'error']
                }
            },
            temperature=0.1)

    if feedback_result['is_error_present']:
        gpt_prompt_feedback({
            'feedback': feedback_result['feedback'],
            'score': score_result['score'],
            'error': score_result['error']
        })

    print('Prompt:\n\n' + str(prompt))
    print('\nFeedback result:\n\n' + str(feedback_result))
    print('\nScore result:\n\n' + str(score_result))
