from pedal.report import MAIN_REPORT, Feedback
import re
import ast

def start_section(name, report=None):
    pass

def next_section(name="", report=None):
    if report is None:
        report = MAIN_REPORT
    if not report['source']['success']:
        return False
    report['source']['section'] += 2
    section = report['source']['section']
    found = len(report['source']['sections'])
    if section < found:
        report['source']['code'] = ''.join(report['source']['sections'][:section+1])
    else:
        report.attach('Verifier Error', category='verifier', tool='Source',
                      section=report['source']['section'],
                      mistakes=("Tried to advance to next section but the "
                                "section was not found. Tried to load section "
                                "{count}, but there were only {found} sections."
                                ).format(count=int(section/2), found=found))
    
def count_sections(count, report=None):
    '''
    Checks that the right number of sections exist. This is not counting the
    prologue, before the first section. So if you have 3 sections in your code,
    you should pass in 3 and not 4.
    '''
    if report is None:
        report = MAIN_REPORT
    if not report['source']['success']:
        return False
    found = int((len(report['source']['sections'])-1)/2)
    if count != found:
        report.attach('Verifier Error', category='verifier', tool='Source',
                      section=report['source']['section'],
                      mistakes=("Incorrect number of sections in your file. "
                                "Expected {count}, but only found {found}"
                                ).format(count=count, found=found))

def verify_section(report=None):
    if report is None:
        report = MAIN_REPORT
    if not report['source']['success']:
        return False
    code = report['source']['code']
    try:
        parsed = ast.parse(code, report['source']['filename'])
        report['source']['ast'] = parsed
    except SyntaxError as e:
        report.attach('Syntax error', category='verifier', tool='Source',
                      section=report['source']['section'],
                      mistakes={'message': "Invalid syntax on line "
                                           +str(e.lineno),
                                'error': e,
                                'position': {"line": e.lineno}})
        report['source']['success'] = False
        if 'ast' in report['source']:
            del report['source']['ast']
    return report['source']['success']
    
class _finish_section:
    def __init__(self, number, *functions):
        if isinstance(number, int):
          self.number = number
        else:
          self.number = -1
          functions = [number] + list(functions)
        self.functions = functions
        for function in functions:
          self(function, False)
    def __call__(self, f=None, quiet=True):
        if f is not None:
          f()
        if quiet:
          print("\tNEXT SECTION")
    def __enter__(self):
        pass
    def __exit__(self, x, y, z):
        print("\tNEXT SECTION")
        #return wrapped_f
def finish_section(number, *functions, next_section=False):
  if len(functions) == 0:
    x = _finish_section(number, *functions)
    x()
  else:
    result = _finish_section(number, *functions)
    if next_section:
      print("\tNEXT SECTION")
    return result

def section(number):
    '''
    '''
    pass

def precondition(function):
    pass
def postcondition(function):
    pass

