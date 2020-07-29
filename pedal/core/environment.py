"""
Environments are a collection of defaults, setups, and overrides that make
Pedal adapt better to a given autograding platform (e.g., BlockPy, WebCAT,
GradeScope). They are meant to streamline common configuration.
"""

__all__ = ['Environment']

from pedal.core.report import MAIN_REPORT
from pedal.core.submission import Submission


class Environment:
    """
    Abstract Environment class, meant to be subclassed by the environment to
    help simplify configuration. Technically doesn't need to do anything.

    Args:
        main_file (str): The filename of the main file.
        main_code (str): The actual code of the main file.
        files (dict[str, str]): A list of filenames mapped to their contents.
    """
    def __init__(self, files=None, main_file='answer.py', main_code=None,
                 user=None, assignment=None, course=None, execution=None,
                 instructor_file='instructor.py', report=MAIN_REPORT):
        self.report = report
        # Setup any code given as the submission.
        if files is None:
            if main_code is None:
                raise ValueError("files and main_code cannot both be None.")
            files = {main_file: main_code}
        else:
            if main_file is not None:
                if main_code is None:
                    main_code = files[main_file]
                if main_file not in files:
                    files[main_file] = main_code
        # Contextualize report
        self.submission = Submission(files, main_file, main_code,
                                     user, assignment, course, execution,
                                     instructor_file)
        self.report.contextualize(self.submission)

    def get_fields(self):
        """ Abstract method to return the interesting fields of this class. """
        return []

    def __iter__(self):
        return self.get_fields()
