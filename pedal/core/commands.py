"""
Imperative style commands for constructing feedback in a convenient way.
Uses a global report object (MAIN_REPORT).
"""

__all__ = ['feedback', 'set_success', 'compliment', 'give_partial', 'explain',
           'gently', 'hide_correctness', 'suppress', 'log', 'debug', 'system_error',
           'clear_report', 'get_all_feedback', 'guidance', 'contextualize_report']

from pedal.core.feedback import Feedback, FeedbackKind, FeedbackCategory, PEDAL_DEVELOPERS, AtomicFeedbackFunction
from pedal.core.report import MAIN_REPORT


#: Lowercase "function" version that works like other Core Feedback Functions.
from pedal.core.submission import Submission

feedback = Feedback


# TODO: force_success function, which ignores errors to give the points.


@AtomicFeedbackFunction(title="Complete",
                        text_template="Great work!".format)
def set_success(score=1, justification=None, tool=None, group=None, report=MAIN_REPORT):
    """
    **(Feedback Function)**

    Creates Successful feedback for the user, indicating that the entire
    assignment is done.

    Args:
        tool:
        group:
        report:
        justification (str): Internal message that explains why this function was used.
        score (number): Arbitrary value to set the user's score to. Defaults to 1.
    """
    return feedback("set_success",
                    tool=tool, category=FeedbackCategory.COMPLETE, kind=FeedbackKind.RESULT,
                    justification=justification, valence=Feedback.POSITIVE_VALENCE,
                    title=set_success.title, message=set_success.text_template(),
                    text=set_success.text_template(),
                    score=score, correct=True,
                    muted=False, version='1.0.0', author=PEDAL_DEVELOPERS, group=group,
                    report=report)


@AtomicFeedbackFunction(title="Compliment")
def compliment(message, value=0, title=None,
               justification=None, locations=None, tool=None, group=None, report=MAIN_REPORT):
    """
    Create a positive feedback for the user, potentially on a specific line of
    code.

    Args:
        title (str): If None, defaults to "Compliment"
        message (str): The message to display to the user.
        locations (int): The relevant line of code to reference.
        value (float): The number to increase the user's score by.
        justification (str): A justification for why this partial credit was given.
    """
    return feedback("compliment", tool=tool,
                    category=FeedbackCategory.INSTRUCTOR, kind=FeedbackKind.ENCOURAGEMENT,
                    justification=justification, locations=locations,
                    valence=Feedback.POSITIVE_VALENCE,
                    title=title or compliment.title, message=message, text=message,
                    score=value, correct=False, muted=False, version='1.0.0',
                    author=PEDAL_DEVELOPERS, group=group, report=report
                    )


@AtomicFeedbackFunction(title="Partial Credit",
                        text_template="Partial credit".format)
def give_partial(value, justification=None, title=None, tool=None, group=None, report=MAIN_REPORT):
    """
    Increases the user's current score by the `value`.

    Args:
        value (number): The number to increase the user's score by.
        justification (str): A justification for why this partial credit was given.
    """
    return feedback("give_partial", tool=tool, category=FeedbackCategory.INSTRUCTOR,
                    kind=FeedbackKind.RESULT,
                    justification=justification, valence=Feedback.POSITIVE_VALENCE,
                    title=title or give_partial.title, message=give_partial.text_template(),
                    text=give_partial.text_template(),
                    score=value, correct=False, muted=True, version='1.0.0', author=PEDAL_DEVELOPERS, group=group,
                    report=report)


@AtomicFeedbackFunction(title="System Error")
def system_error(tool, explanation, author=PEDAL_DEVELOPERS, report=MAIN_REPORT):
    return feedback("system_error", tool=tool, category=Feedback.CATEGORIES.SYSTEM,
                    kind=FeedbackKind.META, justification=explanation,
                    valence=Feedback.NEUTRAL_VALENCE,
                    title=system_error.title, message=explanation, text=explanation,
                    muted=True, author=author, report=report)


@AtomicFeedbackFunction(title="Instructor Feedback")
def explain(message, label='explain', title=None, fields=None,
            justification=None, priority=None, line=None, text=None, score=None, muted=False,
            version='0.0.1', author=None, tags=None, group=None, report=MAIN_REPORT):
    return feedback(label, category=Feedback.CATEGORIES.INSTRUCTOR,
                    kind=FeedbackKind.MISTAKE, justification=justification, priority=priority,
                    valence=Feedback.NEGATIVE_VALENCE, title=title or explain.title,
                    message=message or text, text=text or message,
                    fields=fields or {}, locations=line, score=score, muted=muted, version=version,
                    author=author, tags=tags, group=group or report.group, report=report)


@AtomicFeedbackFunction(title="Instructor Feedback")
def gently(message, label='gently', title=None, fields=None,
           justification=None, priority=Feedback.CATEGORIES.STUDENT, line=None, text=None, score=None, muted=False,
           version='0.0.1', author=None, tags=None, group=None, report=MAIN_REPORT):
    return feedback(label, category=Feedback.CATEGORIES.INSTRUCTOR,
                    kind=FeedbackKind.MISTAKE, justification=justification, priority=priority,
                    valence=Feedback.NEGATIVE_VALENCE, title=title or gently.title,
                    message=message or text, text=text or message,
                    fields=fields or {}, locations=line, score=score, muted=muted, version=version,
                    author=author, tags=tags, group=group or report.group, report=report)


@AtomicFeedbackFunction(title="Instructor Guidance")
def guidance(message, label="guidance", title=None, fields=None,
             justification=None, priority=None, line=None, text=None, score=None,
             muted=False, version='0.0.1', author=None, tags=None, group=None, report=MAIN_REPORT):
    return feedback(label, category=Feedback.CATEGORIES.INSTRUCTIONS,
                    kind=FeedbackKind.INSTRUCTIONAL, justification=justification, priority=priority,
                    valence=Feedback.NEUTRAL_VALENCE, title=title or guidance.title,
                    message=message or text, text=text or message,
                    fields=fields or {}, locations=line, score=score, muted=muted, version=version,
                    author=author, tags=tags, group=group or report.group, report=report)


def hide_correctness(report=MAIN_REPORT):
    report.hide_correctness()


def suppress(category=None, label=True, report=MAIN_REPORT):
    report.suppress(category, label)


def log(message, report=MAIN_REPORT):
    return feedback("log", category=Feedback.CATEGORIES.SYSTEM, muted=True, text=message,
                    valence=Feedback.NEUTRAL_VALENCE)


def debug(message, report=MAIN_REPORT):
    return feedback("debug", category=Feedback.CATEGORIES.SYSTEM, muted=True, text=message,
                    valence=Feedback.NEGATIVE_VALENCE, priority='high')


def clear_report(report=MAIN_REPORT):
    """
    Removes all existing data from the report, including any submissions, suppressions, feedback,
    and Tool data.

    Args:
        report: The report to clear (defaults to the :py:ref:`pedal.core.report.MAIN_REPORT`).
    """
    report.clear()


def contextualize_report(submission, filename='answer.py', clear=True, report=MAIN_REPORT):
    """
    Updates the report with the submission. By default, clears out any old information in the report.
    You can pass in either an actual :py:class:`~pedal.core.submission.Submission` or a string representing
    the code of the submission.

    Args:
        submission (str or Submission):
        filename (str or None): If the `submission` was not a :py:class:`~pedal.core.submission.Submission`,
            then this will be used as the filename for the code given in `submission`.
        report: The report to attach this feedback to (defaults to the :py:ref:`pedal.core.report.MAIN_REPORT`).
    """
    if not isinstance(submission, Submission):
        submission = Submission(files={filename: submission})
    if clear:
        report.clear()
    report.contextualize(submission)


def get_all_feedback(report=MAIN_REPORT) -> [Feedback]:
    """
    Gives access to the list of feedback from the report. Usually, you won't need this; but if you want
    to build on the results of earlier tools, it can be a useful mechanism.

    Args:
        report: The report to attach this feedback to (defaults to the :py:ref:`pedal.core.report.MAIN_REPORT`).

    Returns:
        List[pedal.core.feedback.Feedback]: A list of feedback objects.
    """
    return report.feedback
