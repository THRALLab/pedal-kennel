"""
A package for analyzing student code.
"""
import sys
import os
import logging

logger = logging.getLogger('pedal')
logger.addHandler(logging.NullHandler())
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'ERROR').upper()
)

logger.debug("Pedal import started")

# Core Commands
from pedal.core.report import MAIN_REPORT
from pedal.core.submission import Submission
from pedal.core.commands import *
logger.debug("Pedal core import finished")

from pedal.source import *
logger.debug("Source Tool import finished")

from pedal.sandbox.commands import *
logger.debug("Sandbox Tool import finished")

from pedal.cait import *
logger.debug("CAIT Tool import finished")

from pedal.assertions.commands import *
logger.debug("Assertions Tool import finished")

from pedal.resolvers import *
logger.debug("Resolvers Tool import finished")

student: Sandbox

logger.debug("Pedal import finished")
