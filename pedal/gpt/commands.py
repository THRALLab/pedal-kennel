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

    prompt = f"""{code}"""

    messages = [
        {'role': 'system',
         'content': "You are an intelligent tutor for a introductory computer science course in Python. You never give answers but do give helpful tips guide students with their code."},
        {'role': 'user', 'content': prompt}
    ]

    #print(prompt)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',  # must add -0613 for functions??
        messages=messages,
        functions=[
            {
                'name': 'gpt_prompt_feedback',
                'description': 'Called when there is a problem with the code. ' +
                               'If there are no problems, do not call the function.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'feedback': {
                            'type': 'string',
                            'description': 'Helpful tips to guide a student with their problematic code.'
                        },
                    },
                    'required': ['feedback']
                }
            }
        ],
        function_call={"name": "gpt_prompt_feedback"},
        temperature=1.8,
        top_p=0.5
    )

    #print(response)
    response_message = response.choices[0].message.function_call.arguments

    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=[
            {
                'name': 'gpt_prompt_feedback',
                'description': 'Called when there is a problem with the code. ' +
                               'If there are no problems, do not call the function.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'score': {
                            'type': 'string',
                            'description': 'On a scale 0-10, what would you score their code?'
                        },
                        'error': {
                            'type': 'string',
                            'description': 'List all the error types the code produces.'
                        },
                    },
                    'required': ['score', 'error']
                }
            }
        ],
        function_call={"name": "gpt_prompt_feedback"},
        temperature=0.1,
        top_p=0.5
    )

    #print(second_response)
    second_response_message = second_response.choices[0].message.function_call.arguments

    if second_response.choices[0].message.function_call:
        # todo: handle incorrect responses
        if second_response.choices[0].message.function_call.name == 'gpt_prompt_feedback':
            args = json.loads(second_response_message)
            fields = {
                'feedback': json.loads(response_message)['feedback'],
                'score': args['score'],
                'error': args['error']
            }
            gpt_prompt_feedback(fields)
        else:
            #needs error handling
            print('Invalid function:', second_response_message['function_call']['name'])
    else:
        # needs error handling
        print('Response:', second_response_message['content'])