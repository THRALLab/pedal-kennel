"""
Extensions related to built-in Turtle library.

Mock Module for Sandbox.
"""

from pedal.tifa.builtin_definitions import BUILTIN_MODULES
from pedal.tifa.type_definitions import ModuleType, FunctionType, NoneType

_TURTLE_FIELDS = {
   'forward': FunctionType(name='forward', returns=NoneType()),
   'backward': FunctionType(name='backward', returns=NoneType()),
   'color': FunctionType(name='color', returns=NoneType()),
   'right': FunctionType(name='right', returns=NoneType()),
   'left': FunctionType(name='left', returns=NoneType()),
}
BUILTIN_MODULES['turtle'] = ModuleType('turtle',
                                       fields=_TURTLE_FIELDS),
