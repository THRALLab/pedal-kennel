import json

from pedal import system_error
from pedal.core.report import MAIN_REPORT
from pedal.gpt.constants import TOOL_NAME
from pedal.gpt.feedbacks import gpt_prompt_feedback

try:
    import openai
except ImportError:
    openai = None

__all__ = ['set_openai_api_key', 'gpt_run_prompts']


def set_openai_api_key(key, report=MAIN_REPORT):
    """
    Sets the OpenAI api key in the tool data.

    Args:
        key (str): The API key
        report:
    """
    report[TOOL_NAME]['openai_api_key'] = key


def run_prompt(model, messages, function, temperature=0.5, top_p=0.5, report=MAIN_REPORT):
    """
    Runs a prompt through OpenAI's api which calls a function, and parses the result.

    Args:
        model: The gpt model to use
        messages: A list of messages to pass to the OpenAI api call
        function: The function to pass to the OpenAI api call
        temperature:
        top_p:
        report:
    Returns: A dictionary containing the values of the required arguments, or None if an error is encountered.
             The report is unmodified.
    """
    if not openai:
        return None

    openai.api_key = report[TOOL_NAME]['openai_api_key']
    if not openai.api_key:
        return None

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=[function],
            function_call={'name': function['name']},
            temperature=temperature,
            top_p=top_p
        )
    except openai.error.OpenAIError:
        return None

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


def gpt_run_prompts(code=None, report=MAIN_REPORT, temp_debug_remove_me=False):
    """
    Evaluates the following prompts and attach the results to the Report.

    Args:
        code (str or None): The student's code to evaluate. If ``code`` is not
            given, then it will default to the student's main file.
        report (:class:`pedal.core.report.Report`): The Report object to
            attach results to.
        temp_debug_remove_me (bool): todo(gpt): remove debug prints
    """
    if not openai:
        system_error(TOOL_NAME, 'Could not load OpenAI library!', report=report)
        return
    if not openai.api_key:
        system_error(TOOL_NAME, 'OpenAI API key has not been set!', report=report)
        return

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
        if tries > report[TOOL_NAME]['retry_count']:
            system_error(TOOL_NAME, 'Failed to retrieve valid response from OpenAI!', report=report)
            return

        feedback_result = run_prompt(
            model=report[TOOL_NAME]['model'],
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
            temperature=0.7,
            report=report
        )

    score_result = None
    tries = 0
    while not score_result:
        tries += 1
        if tries > report[TOOL_NAME]['retry_count']:
            system_error(TOOL_NAME, 'Failed to retrieve valid response from OpenAI!', report=report)
            return

        score_result = run_prompt(
            model=report[TOOL_NAME]['model'],
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
            temperature=0.1,
            report=report
        )

    if feedback_result['is_error_present']:
        gpt_prompt_feedback({
            'feedback': feedback_result['feedback'],
            'score': score_result['score'],
            'error': score_result['error']
        })

    if temp_debug_remove_me:
        print('Prompt:\n\n' + str(prompt))
        print('\nFeedback result:\n\n' + str(feedback_result))
        print('\nScore result:\n\n' + str(score_result))
