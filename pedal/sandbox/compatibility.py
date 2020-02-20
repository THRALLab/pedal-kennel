import sys

from pedal.sandbox.sandbox import Sandbox
from pedal.sandbox.messages import EXTENDED_ERROR_EXPLANATION

from pedal.core.report import MAIN_REPORT


def _check_sandbox(report=MAIN_REPORT):
    if 'run' not in report['sandbox']:
        report['sandbox']['run'] = Sandbox()
    return report['sandbox']['run']


def run_student(raise_exceptions=False, report=MAIN_REPORT, old_style_messages=False):
    sandbox = _check_sandbox(report)
    source_code = report['source']['code']
    filename = report['source']['filename']
    sandbox.run(source_code, as_filename=filename, report_exceptions=not raise_exceptions)
    if raise_exceptions:
        raise_exception(sandbox.exception, sandbox.exception_position,
                        report=report, message=None if old_style_messages else sandbox.exception_formatted)
    return sandbox.exception


def queue_input(*inputs, **kwargs):
    if 'report' not in kwargs:
        report = MAIN_REPORT
    else:
        report = kwargs['report']
    sandbox = _check_sandbox(report)
    sandbox.set_input(inputs)


def reset_output(report=MAIN_REPORT):
    sandbox = _check_sandbox(report)
    sandbox.set_output(None)


def get_output(report=MAIN_REPORT):
    sandbox = _check_sandbox(report)
    return sandbox.output


def get_plots(report=MAIN_REPORT):
    sandbox = _check_sandbox(report)
    if 'matplotlib.pyplot' in sandbox.modules:
        mock_plt = sandbox.modules['matplotlib.pyplot']
        if hasattr(mock_plt, 'plots'):
            return mock_plt.plots
    return []


def capture_output(function, *args, **kwargs):
    if 'report' in kwargs:
        report = kwargs['report']
    else:
        report = MAIN_REPORT
    sandbox = _check_sandbox(report)
    sandbox.set_output(None)
    sandbox.call(function.__name__, *args)
    return sandbox.output


def get_sandbox(report=MAIN_REPORT):
    sandbox = _check_sandbox(report)
    return sandbox


def raise_exception(exception, position=None, report=MAIN_REPORT, message=None):
    sandbox = _check_sandbox(report)
    if exception is None:
        return
    extended = EXTENDED_ERROR_EXPLANATION.get(exception.__class__, "")
    if message is None:
        message = "<pre>{}</pre>\n{}".format(str(exception), extended)
    # Skulpt compatible name lookup
    name = str(exception.__class__)[8:-2]
    report.attach(name, category='Runtime', tool='Sandbox',
                  mistake={'message': message,
                           'error': exception,
                           'position': position,
                           'traceback': None})
    sandbox.exception = exception


def get_student_data(report=MAIN_REPORT):
    sandbox = _check_sandbox(report)
    return sandbox


def set_sandbox(sandbox, report=MAIN_REPORT):
    """
    Update the sandbox to hold the new sandbox instance. Particularly useful
    for Skulpt, which needs to set the sandbox in an unusual way.
    """
    report['sandbox']['run'] = sandbox
    return sandbox


def trace_lines(report=MAIN_REPORT):
    sandbox = _check_sandbox(report)
    if sandbox.tracer_style == 'coverage':
        return sandbox.trace.lines - sandbox.trace.missing
    else:
        return []
