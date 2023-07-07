"""
Initialize and setup the OpenAI tool.
"""

from pedal.core.report import MAIN_REPORT, Report
from pedal.gpt.constants import TOOL_NAME


def reset(report=MAIN_REPORT):
    """
    Remove all settings for the OpenAI tool.

    Args:
        report: The report object

    Returns:
        This tool's data
    """
    report[TOOL_NAME] = {
        'model': 'gpt-3.5-turbo-0613',  # 'gpt-4-0613'
        'retry_count': 3
    }
    return report[TOOL_NAME]


Report.register_tool(TOOL_NAME, reset)
