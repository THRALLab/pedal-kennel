"""
Initialize and setup the OpenAI tool.
"""

from pedal.core.report import MAIN_REPORT, Report
from pedal.gpt.commands import gpt_get_default_prompts
from pedal.gpt.constants import TOOL_NAME
import os


def reset(report=MAIN_REPORT):
    """
    Remove all settings for the OpenAI tool.

    Args:
        report: The report object

    Returns:
        This tool's data
    """
    report[TOOL_NAME] = {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),  # Will be None if the env var doesn't exist
        'model': 'gpt-3.5-turbo-0613',  # 'gpt-4-0613',
        'prompts_getter': gpt_get_default_prompts,
        'retry_count': 3
    }
    return report[TOOL_NAME]


Report.register_tool(TOOL_NAME, reset)
