"""
Initialize and setup the OpenAI tool.
"""

from pedal.core.report import MAIN_REPORT, Report
from pedal.gpt.constants import TOOL_NAME

#we need setup.py?
def reset(report=MAIN_REPORT):
    """
    Remove all settings for the OpenAI tool.

    Args:
        report: The report object

    Returns:
        This tool's data
    """
    report[TOOL_NAME] = {}
    return report[TOOL_NAME]


Report.register_tool(TOOL_NAME, reset)
