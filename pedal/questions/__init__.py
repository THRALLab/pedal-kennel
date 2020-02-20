"""
A tool for providing dynamic questions to learners.
"""

NAME = 'Questions'
SHORT_DESCRIPTION = "Provides dynamic questions to learners"
DESCRIPTION = '''
'''
REQUIRES = []
OPTIONALS = []
CATEGORY = 'Instructions'

__all__ = ['NAME', 'DESCRIPTION', 'SHORT_DESCRIPTION', 'REQUIRES', 'OPTIONALS',
           'Question', 'Pool', 'set_seed']

from pedal.questions.setup import _setup_questions, set_seed, _name_hash
from pedal.questions.loader import load_question, SETTING_SHOW_CASE_DETAILS
from pedal.questions.questions import Question
from pedal.questions.pool import Pool


