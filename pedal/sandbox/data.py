"""
Helper classes for storing data about executions.

NameSpace
    A dictionary that maps names to values. Represents the results of executing
    code, specifically the variables/functions/classes/etc. that exist
    afterwards. Think of it as "locals()". Represented to instructors via
    the `data` attribute.

Context
    The code that was previously executed. This is a history of what was
    executed, that can be used to augment stack traces and such. There are
    commands available to "chunk" contexts so that executions can be grouped
    as a single series of concepts.

Context ID
    A unique identifier for an execution

Execute
    Given some Python code, AST, or filename, uses ``compile`` and ``exec``
    to actually run the code.

Run
    To execute an arbitrary chunk of code, as opposed to being a ``call`` or
    ``eval``.

Call
    To execute a specific function that exists in the current NameSpace.

Eval
    To execute a chunk of code that represents an expression, storing the
    result in a temporary variable.

Target
    When code is Called or Evaled, the result is stored in a Target. This
    can be a variable, or a more complex expression.
"""
from pedal.sandbox.mocked import MockDictModule, MockModule, create_module


class SandboxContextKind:
    """ Enumeration of sandbox execution kind's. """
    RUN = 'run'
    EVAL = 'eval'
    CALL = 'call'


class SandboxContext:
    """
    Simple data class holding information about an execution within a sandbox.
    Includes such information as the code that was run, its filename, inputs,
    outputs, exceptions, etc.

    Args:
        call_id (int): The unique ID representing this sandbox execution.
        code (str): The code that was executed.
        filename (str): The filename of the code that was executed.
        kind (SandboxContextKind): The kind of execution that generated this.
        target (str or None): If the result was stored in a variable/expression,
            this will be its name.
        inputs (list[str]): Any inputs that were used during the code's
            execution.
        output (str): The output that was generated by this execution.
        exception (Exception or None): The exception that occurred during this
            execution, or None if none occurred.
        submission (:py:class:`pedal.core.submission.Submission`): The
            submission object that this context was attached to.
    """

    def __init__(self, call_id, code, filename, kind, target, inputs, output,
                 exception, submission):
        self.call_id = call_id
        self.kind = kind
        self.code = code
        self.filename = filename
        self.target = target
        self.inputs = inputs
        self.output = output
        self.exception = exception
        self.submission = submission


def format_contexts(contexts):
    """
    Create a text string representation from a list of contexts.

    Args:
        contexts (list[SandboxContext]): The list of sandbox executions.

    Returns:
        str: The string representation of the contexts.
    """
    execution_text = []
    inputs_text = []
    for context in contexts:
        if context.filename in (None, context.submission.instructor_file):
            execution_text.append(f"I ran the code:\n<pre>{context.code}</pre>\n")
        else:
            execution_text.append(f"I ran the file `{context.filename}`.\n")
        inputs_text.extend(context.inputs)
    final_text = []
    final_text.extend(execution_text)
    if inputs_text:
        final_text.append("And I entered as input:\n<pre>{}</pre>\n".format(
            "\n".join(inputs_text)
        ))
    return "\n".join(final_text)


class SandboxModules:
    """
    Container for any mocked modules and their data.
    """

    def __init__(self):
        self._modules = {}

    def clear(self):
        """ Removes any existing modules. """
        self._modules.clear()

    def new_module(self, data, import_name, friendly_name):
        """
        Creates a new mocked module.

        Args:
            data (dict or MockModule): The data to use for the new mocked module
            import_name (str): The name that is associated with ``import``.
            friendly_name (str): The name to use when accessing this module's
                data via attribute lookup.

        Returns:
            dict[str,:py:class:`types.ModuleType`]: The newly created modules
                mapped by their imported path names.
        """
        root, modules, target = create_module(import_name)
        if isinstance(data, dict):
            mocked_module = MockDictModule(data)
            mocked_module.add_to_module(target)
        elif isinstance(data, MockModule):
            data.add_to_module(target)
        else:
            raise ValueError("Given data must be either MockModule or dict.")
        self._modules[friendly_name] = data
        return modules

    def __getattr__(self, name):
        return self._modules[name]

    def __dir__(self):
        return self._modules.keys()


class SandboxVariable:
    """
    A representation of a variable in the student's data namespace. This
    has limited application, but can be used to improve the data passed into
    :py:func:`pedal.sandbox.commands.call` so that the local variables are used.
    Largely superceded by the ``locals_args`` parameter.
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value
