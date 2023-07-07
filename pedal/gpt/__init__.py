from pedal.gpt.setup import reset
from pedal.gpt.commands import set_openai_api_key, gpt_run_prompts

NAME = 'GPT'
SHORT_DESCRIPTION = "Runs code and other tool results through an OpenAI LLM"
DESCRIPTION = '''
'''
REQUIRES = []
OPTIONALS = []
CATEGORY = "highest"

__all__ = ['NAME', 'DESCRIPTION', 'SHORT_DESCRIPTION', 'REQUIRES', 'OPTIONALS',
           'set_openai_api_key', 'gpt_run_prompts']
