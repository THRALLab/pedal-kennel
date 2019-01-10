'''
A package for verifying source code.
'''

from pedal.report import MAIN_REPORT, Feedback
import re
import ast

NAME = 'Source'
SHORT_DESCRIPTION = "Verifies source code and attaches it to the report"
DESCRIPTION = '''
'''
REQUIRES = []
OPTIONALS = []
CATEGORY = 'Syntax'

__all__ = ['NAME', 'DESCRIPTION', 'SHORT_DESCRIPTION', 'REQUIRES', 'OPTIONALS',
           'set_source', 'count_sections', 'next_section', 'verify_section',
           'precondition', 'postcondition', 'finish_section', 'section']
DEFAULT_PATTERN = r'^(##### Part .+)$'

def set_source(code, filename='__main__.py', sections=False, report=None):
    '''
    Sets the contents of the Source to be the given code. Can also be
    optionally given a filename.
    
    Args:
        code (str): The contents of the source file.
        filename (str): The filename of the students' code. Defaults to
                        __main__.py. 
        sections (str or bool): Whether or not the file should be divided into
                                sections. If a str, then it should be a
                                Python regular expression for how the sections
                                are separated. If False, there will be no
                                sections. If True, then the default pattern
                                will be used: '^##### Part (\d+)$'
        report (Report): The report object to store data and feedback in. If
                         left None, defaults to the global MAIN_REPORT.
    '''
    if report is None:
        report = MAIN_REPORT
    report['source']['code'] = code
    report['source']['filename'] = filename
    report['source']['success'] = True
    if sections == False:
        report['source']['sections'] = None
        report['source']['section'] = None
        _check_issues(code, report)
    else:
        if sections == True:
            pattern = DEFAULT_PATTERN
        else:
            pattern = sections
        report['source']['section_pattern'] = pattern
        report['source']['section'] = 0
        report['source']['sections'] = re.split(pattern, code,
                                                flags=re.MULTILINE)
        report['source']['code'] = report['source']['sections'][0]

def _check_issues(code, report):
    if code.strip() == '':
        report.attach('Blank source', category=CATEGORY, tool=NAME,
                      section=report['source']['section'],
                      mistakes="Source code file is blank.")
        report['source']['success'] = False
    try:
        parsed = ast.parse(code, report['source']['filename'])
        report['source']['ast'] = parsed
    except SyntaxError as e:
        report.attach('Verifier Error', category='verifier', tool='Source',
                      section=report['source']['section'],
                      mistakes={'message': "Invalid syntax on line "
                                           +str(e.lineno),
                                'error': e,
                                'position': {"line": e.lineno}})
        report['source']['success'] = False
        if 'ast' in report['source']:
            del report['source']['ast']

def get_program(report=None):
    if report is None:
        report = MAIN_REPORT
    return report['source']['code']

from pedal.source.sections import *
