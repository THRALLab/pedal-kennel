import json
import time

from pedal import system_error
from pedal.core.report import MAIN_REPORT
from pedal.gpt.constants import TOOL_NAME
from pedal.gpt.feedbacks import gpt_prompt_feedback

try:
    import openai
except ImportError:
    openai = None

__all__ = ['set_openai_api_key', 'gpt_get_default_prompts', 'gpt_run_prompts']


def set_openai_api_key(key, report=MAIN_REPORT):
    """
    Sets the OpenAI api key in the tool data.

    Args:
        key (str): The API key
        report:
    """
    report[TOOL_NAME]['openai_api_key'] = key


def gpt_get_default_prompts(code=None, report=MAIN_REPORT):
    """
    Returns each prompt to run, as well as the processing function that generates feedback
    from the results. If there is an error at any point, the processing function is never called.

    Args:
        code (str or None): The student's code to evaluate. If ``code`` is not
            given, then it will default to the student's main file.
        report (:class:`pedal.core.report.Report`): The Report object to
            attach results to.
    """
    shared_messages = [
        {
            'role': 'system',
            'content': "You are an intelligent tutor for a introductory computer science course in Python. " +
                       "You never give answers but do give helpful tips to guide students with their code."
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
    score_function = {
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
    }

    prompts = {
        'feedback': (shared_messages, feedback_function, 0.7, 0.5),
        # 'score': (shared_messages, score_function, 0.1, 0.5)
    }

    def process_prompts(results):
        # if results['feedback']['is_error_present']:
        gpt_prompt_feedback({
            'feedback': results['feedback']['feedback'],
            # 'score': results['score']['score'],
            # 'error': results['score']['error']
        })

        # Debug code
        print('Feedback result:\n' + str(results['feedback']))
        # print('Score result:\n' + str(results['score']))
        print()

    return prompts, process_prompts


def run_prompt(model, messages, function, temperature, top_p, report=MAIN_REPORT):
    """
    Runs a prompt through OpenAI's api which calls a function, and parses the result.

    Args:
        model: The gpt model to use
        messages: A list of messages to pass to the OpenAI api call
        function: The function to pass to the OpenAI api call
        temperature:
        top_p:
        report (:class:`pedal.core.report.Report`): The Report object to read the OpenAI API key from.
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
    except openai.error.RateLimitError:
        # todo: report this somewhere
        time.sleep(21)  # yikes, need to make this configurable or optionally ignore this error
        return run_prompt(model, messages, function, temperature, top_p, report)
    except openai.error.OpenAIError as e:
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


def gpt_run_prompts(code=None, report=MAIN_REPORT):
    """
    Evaluates the prompts stored in tool data and attach the results to the Report.

    Args:
        code (str or None): The student's code to evaluate. If ``code`` is not
            given, then it will default to the student's main file.
        report (:class:`pedal.core.report.Report`): The Report object to
            attach results to.
    """
    if not openai:
        raise ImportError('Could not load OpenAI library!')
    if not openai.api_key:
        raise openai.OpenAIError('OpenAI API key has not been set!')

    if not code:
        code = report.submission.main_code  # what if no code in file + no main code?

    prompts, process_prompts = report[TOOL_NAME]['prompts_getter'](code, report=report)
    results = {}

    for prompt in prompts:
        prompt_data = prompts[prompt]

        result = None
        tries = 0
        while not result:
            tries += 1
            if tries > report[TOOL_NAME]['retry_count']:
                raise openai.OpenAIError('Failed to retrieve valid response from OpenAI!')

            result = run_prompt(
                model=report[TOOL_NAME]['model'],
                messages=prompt_data[0],
                function=prompt_data[1],
                temperature=prompt_data[2],
                top_p=prompt_data[3],
                report=report
            )

        results[prompt] = result

        # Debug code
        print('PROMPT: ' + prompt)
        print('------')
        print('Messages:\n' + str(prompt_data[0]))
        print('Function:\n' + str(prompt_data[1]))
        print('Temperature: ' + str(prompt_data[2]))
        print('Top P: ' + str(prompt_data[3]))
        print()

    process_prompts(results)
