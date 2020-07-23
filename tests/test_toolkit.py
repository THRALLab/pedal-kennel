import unittest
import os
import sys
from textwrap import dedent

from pedal.assertions.static import prevent_operation, ensure_operation, function_prints
from pedal.cait.find_node import find_operation, find_prior_initializations, find_function_calls, is_top_level, \
    function_is_called
from pedal.core.commands import suppress
from pedal.core.feedback import Feedback
from pedal.core.report import MAIN_REPORT
from pedal.toolkit.records import check_record_instance

pedal_library = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, pedal_library)

here = "" if os.path.basename(os.getcwd()) == "tests" else "tests/"

from pedal.core import *
from pedal.source import set_source

from pedal.cait.cait_api import parse_program
from pedal.sandbox.sandbox import Sandbox
from pedal.toolkit.files import files_not_handled_correctly
from pedal.toolkit.functions import (match_signature, output_test, unit_test,
                                     check_coverage, match_parameters)
from pedal.toolkit.signatures import (function_signature)
from pedal.toolkit.imports import ensure_imports
from pedal.toolkit.printing import ensure_prints
from pedal.extensions.plotting import check_for_plot, prevent_incorrect_plt
from tests.execution_helper import Execution, ExecutionTestCase


class TestFiles(ExecutionTestCase):

    def test_files_not_closed(self):
        with Execution('open("not opened.txt")') as e:
            self.assertTrue(files_not_handled_correctly(1))
        self.assertFeedback(e, "Unclosed Files\nYou have not closed all the files you "
                                "were supposed to.")

    def test_files_closed_as_function(self):
        with Execution('open("not opened.txt")\nclose()') as e:
            self.assertTrue(files_not_handled_correctly(1))
        self.assertFeedback(e, "Close Is a Method\nYou have attempted to call "
                                    "`close` as a function, but it is "
                                    "actually a method of the file object.")

    def test_files_open_without_filename(self):
        with Execution('open()') as e:
            self.assertTrue(files_not_handled_correctly(1))
        self.assertEqual(e.final.message, "You have called the `open` "
                                    "function without any arguments. It needs a "
                                    "filename.")

    def test_files_open_as_method(self):
        with Execution('"filename.txt".open()') as e:
            self.assertTrue(files_not_handled_correctly(1))
        self.assertEqual(e.final.message, "You have attempted to call "
                                    "`open` as a method, but it is actually a "
                                    "built-in function.")

    def test_files_not_all_files_opened(self):
        with Execution('a = open("A.txt")\na.close()') as e:
            self.assertTrue(files_not_handled_correctly(2))
        self.assertEqual(e.final.message, "You have not opened all the files you "
                                    "were supposed to.")

    def test_files_too_many_opens(self):
        with Execution('a = open("A.txt")\nb = open("B.txt")'
                       '\na.close()\nb.close()') as e:
            self.assertTrue(files_not_handled_correctly(1))
        self.assertEqual(e.final.message, "You have opened more files than you "
                                    "were supposed to.")

    def test_files_too_many_closes(self):
        with Execution('a = open("A.txt")\n\na.close()\na.close()') as e:
            self.assertTrue(files_not_handled_correctly(1))
        self.assertEqual(e.final.message, "You have closed more files than you "
                                    "were supposed to.")

    def test_files_too_many_with_opens(self):
        with Execution('with open("A.txt") as out:\n  b = open("B.txt")'
                       '\n  b.close()') as e:
            self.assertTrue(files_not_handled_correctly(1))
        self.assertEqual(e.final.message, "You have opened more files than you "
                                    "were supposed to.")

    def test_files_missing_filename(self):
        with Execution('with open("A.txt") as out:\n  print(out.read())') as e:
            self.assertTrue(files_not_handled_correctly("X.txt"))
        self.assertEqual(e.final.message, "You must use the literal value "
                                    "`'X.txt'`.")

    def test_files_with_open_success(self):
        with Execution('with open("A.txt") as out:\n  print(out.read())') as e:
            self.assertFalse(files_not_handled_correctly("A.txt"))
            suppress(Feedback.CATEGORIES.RUNTIME)
        self.assertEqual(e.final.message, "No errors reported.")

        with Execution('a = open("filename.txt")\na.close()') as e:
            self.assertFalse(files_not_handled_correctly(1))


class TestFunctions(unittest.TestCase):

    def test_match_signature(self):
        with Execution('a = 0\na') as e:
            self.assertIsNone(match_signature('a', 0))
        self.assertEqual(e.final.message, "No function named <code>a</code> "
                                    "was found.")

        with Execution('def a():\n  pass\na') as e:
            self.assertIsNotNone(match_signature('a', 0))
        self.assertNotEqual(e.final.message, "No function named <code>a</code> "
                                       "was found.")

        with Execution('def a():\n  pass\na') as e:
            self.assertIsNone(match_signature('a', 1))
        self.assertNotEqual(e.final.message, "The function named <code>a</code> "
                                       "has fewer parameters (0) than expected (1)")

        with Execution('def a(x, y):\n  pass\na') as e:
            self.assertIsNone(match_signature('a', 1))
        self.assertNotEqual(e.final.message, "The function named <code>a</code> "
                                       "has fewer parameters (2) than expected (1)")

        with Execution('def a(l, m):\n  pass\na') as e:
            self.assertIsNone(match_signature('a', 2, 'x', 'y'))
        self.assertEqual(e.final.message, "Error in definition of "
                                    "<code>a</code>. Expected a parameter named "
                                    "x, instead found l.")

        with Execution('def a(x, y):\n  pass\na') as e:
            self.assertIsNotNone(match_signature('a', 2, 'x', 'y'))
        self.assertNotEqual(e.final.message, "Error in definition of "
                                       "<code>a</code>. Expected a parameter named "
                                       "x, instead found l.")

    def test_match_parameters(self):
        with Execution('def a(x:str, y:int):\n  pass\na') as e:
            self.assertIsNone(match_parameters('a', int, "int"))
        self.assertEqual(e.final.message,
                "Error in definition of function `a` parameter `x`. "
                "Expected `int`, instead found `str`.")

        with Execution('def a(x:int, y:int):\n  pass\na') as e:
            self.assertIsNotNone(match_parameters('a', int, "int"))
        self.assertNotEqual(e.final.message, "Error in definition of "
                                       "function `a`. Expected `int` parameter, instead found `str`.")

        with Execution('def a(x:[str], y:{int:str}):\n  pass\na') as e:
            self.assertIsNotNone(match_parameters('a', "[str]", "{int:str}"))
        self.assertNotEqual(e.final.message,
                "Error in definition of function `a` parameter `x`. "
                "Expected `int`, instead found `str`.")

        with Execution('def a(x:[str], y:{int:str}):\n  pass\na') as e:
            self.assertIsNotNone(match_parameters('a', "[str]", {int:str}))
        self.assertNotEqual(e.final.message,
                "Error in definition of function `a` parameter `x`. "
                "Expected `int`, instead found `str`.")

        with Execution('def a(x:{str:[bool]}):\n  pass\na') as e:
            self.assertIsNone(match_parameters('a', "{int: [bool]}"))
        self.assertEqual(e.final.message,
                "Error in definition of function `a` parameter `x`. "
                "Expected `{int: [bool]}`, instead found `{str: [bool]}`.")

        with Execution('def a(x:int)->int:\n  pass\na') as e:
            self.assertIsNotNone(match_parameters('a', int, returns=int))
        self.assertNotEqual(e.final.message, "Not right")

        with Execution('def a(x:int)->int:\n  pass\na') as e:
            self.assertIsNone(match_parameters('a', int, returns=str))
        self.assertEqual(e.final.message, "Error in definition of function `a` return type. Expected `str`, instead "
                                          "found int.")

    def test_unit_test(self):
        # All passing
        with Execution('def a(x,y):\n  return(x+y)\na') as e:
            self.assertIsNotNone(unit_test('a', (1, 2, 3)))
        self.assertEqual(e.final.message, "No errors reported.")

        # All failing
        with Execution('def a(x,y):\n  return(x-y)\na') as e:
            self.assertIsNone(unit_test('a', (1, 2, 3)))
        self.assertIn("it failed 1/1 tests", e.final.message)

        # Some passing, some failing
        with Execution('def a(x,y):\n  return(x-y)\na') as e:
            self.assertIsNone(unit_test('a', (1, 2, 3), (0, 0, 0)))
        self.assertIn("it failed 1/2 tests", e.final.message)

        # Optional tip
        with Execution('def a(x,y):\n  return(x-y)\na') as e:
            self.assertIsNone(unit_test('a', (1, 2, (3, "Try again!"))))
        self.assertIn("it failed 1/1 tests", e.final.message)
        self.assertIn("Try again!", e.final.message)

        # Float precision
        with Execution('def a(x,y):\n  return(x+y)\na') as e:
            self.assertIsNotNone(unit_test('a', (1.0, 2.0, 3.0)))
        self.assertEqual(e.final.message, "No errors reported.")

        # Not a function
        with Execution('a = 5\na') as e:
            self.assertIsNone(unit_test('a', (1, 2, 3)))
        self.assertEqual(e.final.message, "You defined a, but did not define "
                                    "it as a function.")

        # Not defined
        with Execution('x = 5\nx') as e:
            self.assertIsNone(unit_test('a', (1, 2, 3)))
        self.assertEqual(e.final.message, "The function <code>a</code> was "
                                    "not defined.")

    def test_output_test(self):
        # All passing
        with Execution('def a(x):\n  print(x+1)\na(1)') as e:
            self.assertIsNotNone(output_test('a', (2, "3")))
        self.assertEqual(e.final.message, "No errors reported.")

        # All failing
        with Execution('def a(x,y):\n  print(x-y)\na(1,2)') as e:
            self.assertIsNone(output_test('a', (1, 2, "3")))
        self.assertIn("wrong output 1/1 times", e.final.message)

        # All passing, multiline
        with Execution('def a(x):\n  print(x+1)\n  print(x+2)\na(1)') as e:
            self.assertIsNotNone(output_test('a', (4, ["5", "6"])))
        self.assertEqual(e.final.message, "No errors reported.")

    def test_check_coverage(self):
        test_files = [
            (here+'sandbox_coverage/bad_non_recursive.py', {4}),
            (here+'sandbox_coverage/good_recursive.py', False),
            (here+'sandbox_coverage/complex.py', {7, 9, 10, 11, 12, 13, 14, 15}),
        ]
        for TEST_FILENAME, missing_lines in test_files:
            with open(TEST_FILENAME) as student_file:
                student_code = student_file.read()
            set_source(student_code, report=MAIN_REPORT)
            student = Sandbox()
            student.tracer_style='coverage'
            student.run(student_code, filename=TEST_FILENAME)
            uncovered, percentage = check_coverage()
            self.assertEqual(uncovered, missing_lines)


class TestUtilities(unittest.TestCase):
    def test_is_top_level(self):
        with Execution('print("Test")\ndef a(x):\n  print(x+1)\na(1)') as e:
            ast = parse_program()
            defs = ast.find_all('FunctionDef')
            self.assertEqual(len(defs), 1)
            self.assertTrue(is_top_level(defs[0]))
            self.assertEqual(len(defs[0].body), 1)
            self.assertFalse(is_top_level(defs[0].body[0]))
            calls = ast.find_all('Call')
            self.assertEqual(len(calls), 3)
            self.assertTrue(is_top_level(calls[0]))
            self.assertFalse(is_top_level(calls[1]))
        self.assertEqual(e.final.message, "No errors reported.")

    def test_function_prints(self):
        # Function prints
        with Execution('def a(x):\n  print(x+1)\na(1)') as e:
            self.assertTrue(function_prints())
        self.assertEqual(e.final.message, "No errors reported.")
        # Function only returns, no prints
        with Execution('def a(x):\n  return x+1\na(1)') as e:
            self.assertFalse(function_prints())
        self.assertEqual(e.final.message, "No errors reported.")
        # Function does not print, but prints exist
        with Execution('print("T")\ndef a(x):\n  x\na(1)\nprint("E")') as e:
            self.assertFalse(function_prints())
        self.assertEqual(e.final.message, "No errors reported.")

    def test_find_function_calls(self):
        with Execution('def a(x):\n  print(x,1)\na(1)\nprint("T")') as e:
            prints = find_function_calls('print')
            self.assertEqual(len(prints), 2)
            self.assertEqual(len(prints[0].args), 2)
            self.assertEqual(len(prints[1].args), 1)
        self.assertEqual(e.final.message, "No errors reported.")
        with Execution('a=[]\na.append(a)\na.pop()\n') as e:
            pops = find_function_calls('pop')
            self.assertEqual(len(pops), 1)
            self.assertEqual(len(pops[0].args), 0)
        self.assertEqual(e.final.message, "No errors reported.")

    def test_function_is_called(self):
        with Execution('a=[]\na.append(a)\na.pop()\n') as e:
            self.assertTrue(function_is_called('pop'))
            self.assertFalse(function_is_called('print'))
        self.assertEqual(e.final.message, "No errors reported.")


    def test_find_prior_initializations(self):
        with Execution('a=0\na\na=5\na') as e:
            ast = parse_program()
            self.assertEqual(len(ast.body), 4)
            self.assertEqual(ast.body[3].ast_name, "Expr")
            self.assertEqual(ast.body[3].value.ast_name, "Name")
            priors = find_prior_initializations(ast.body[3].value)
            self.assertEqual(len(priors), 2)





    def test_prevent_advanced_iteration(self):
        with Execution('while False:\n  pass') as e:
            prevent_advanced_iteration()
        self.assertEqual(e.final.message, "You should not use a <code>while</code> "
                                    "loop to solve this problem.")
        with Execution('sum([1,2,3])') as e:
            prevent_advanced_iteration()
        self.assertEqual(e.final.message, "You cannot use the builtin function "
                                    "<code>sum</code>.")

    def test_find_operation(self):
        with Execution('1+1') as e:
            ast = parse_program()
            self.assertNotEqual(find_operation("+", ast), False)
        with Execution('1>1') as e:
            ast = parse_program()
            self.assertNotEqual(find_operation(">", ast), False)
        with Execution('True and True') as e:
            ast = parse_program()
            self.assertNotEqual(find_operation("and", ast), False)
        with Execution('not True') as e:
            ast = parse_program()
            self.assertNotEqual(find_operation("not", ast), False)
        with Execution('not (1 + 1) and 1 < 1 <= 10') as e:
            ast = parse_program()
            self.assertFalse(find_operation(">", ast))
        with Execution('1 in [1,2,3]') as e:
            ast = parse_program()
            self.assertNotEqual(find_operation("in", ast), False)

    def test_ensure_assignment(self):
        with Execution('a=0') as e:
            self.assertNotEqual(ensure_assignment("a", "Num"), False)
        with Execution('a=""') as e:
            self.assertNotEqual(ensure_assignment("a", "Str"), False)
        with Execution('a=True') as e:
            self.assertNotEqual(ensure_assignment("a", "Bool"), False)


class TestImports(unittest.TestCase):
    def test_ensure_imports(self):
        with Execution('json = "0"\njson.loads("0")+0') as e:
            self.assertTrue(ensure_imports("json"))
        self.assertEqual(e.final.message, "You need to import the <code>json</code> "
                                    "module.")
        with Execution('from requests import json\njson.loads("0")+0') as e:
            self.assertTrue(ensure_imports("json"))
        self.assertEqual(e.final.message, "You need to import the <code>json</code> "
                                    "module.")
        with Execution('import json\njson.loads("0")+0') as e:
            self.assertFalse(ensure_imports("json"))
        self.assertEqual(e.final.message, "No errors reported.")
        with Execution('from json import loads\nloads("0")+0') as e:
            self.assertFalse(ensure_imports("json"))
        self.assertEqual(e.final.message, "No errors reported.")


class TestPrints(unittest.TestCase):
    def test_ensure_prints(self):
        with Execution('print(1)\nprint(2)') as e:
            self.assertFalse(ensure_prints(1))
        self.assertEqual(e.final.message, "You are printing too many times!")
        with Execution('print(1)\nprint(2)') as e:
            self.assertFalse(ensure_prints(3))
        self.assertEqual(e.final.message, "You are not printing enough things!")
        with Execution('a = 0\na') as e:
            self.assertFalse(ensure_prints(1))
        self.assertEqual(e.final.message, "You are not using the print function!")
        with Execution('def x():\n  print(x)\nx()') as e:
            self.assertFalse(ensure_prints(1))
        self.assertEqual(e.final.message, "You have a print function that is not at "
                                    "the top level. That is incorrect for "
                                    "this problem!")
        with Execution('print(1)\nprint(2)') as e:
            prints = ensure_prints(2)
            self.assertNotEqual(prints, False)
            self.assertEqual(len(prints), 2)
        self.assertEqual(e.final.message, "No errors reported.")


class TestPlots(unittest.TestCase):
    def test_check_for_plot(self):
        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.hist([1,2,3])
            plt.title("My line plot")
            plt.show()
            plt.plot([4,5,6])
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('hist', [1, 2, 3]), False)
        self.assertEqual(e.final.message, "No errors reported.")

        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('hist', [1, 2, 3, 4]),
                             "You have created a histogram, but it does not "
                             "have the right data.<br><br><i>(wrong_plt_data)<i></br></br>")

        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('line', [4, 5, 6]), False)
        self.assertEqual(e.final.message, "No errors reported.")

        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('line', [4, 5, 6, 7]),
                             "You have created a line plot, but it does not "
                             "have the right data.<br><br><i>(wrong_plt_data)<i></br></br>")

        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1,2,3])
            plt.title("My line plot")
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('hist', [1, 2, 3]),
                             "You have plotted the right data, but you appear "
                             "to have not plotted it as a histogram.<br><br><i>(wrong_plt_type)<i></br></br>")

        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1,2,3])
            plt.title("Wrong graph with the right data")
            plt.show()
            plt.hist([4,5,6])
            plt.title("Right graph with the wrong data")
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('hist', [1, 2, 3]),
                             "You have created a histogram, but it does not "
                             "have the right data. That data appears to have "
                             "been plotted in another graph.<br><br><i>(other_plt)<i></br></br>")

        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1,2,3])
            plt.title("My line plot")
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('hist', [4, 5, 6]),
                             "You have not created a histogram with the "
                             "proper data.<br><br><i>(no_plt)<i></br></br>")

        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.scatter([], [])
            plt.title("Nothingness and despair")
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('scatter', []), False)

        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.scatter([1,2,3], [4,5,6])
            plt.title("Some actual stuff")
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(check_for_plot('scatter', [[1, 2, 3], [4, 5, 6]]),
                             False)

    def test_prevent_incorrect_plt(self):
        student_code = dedent('''
            import matplotlib.pyplot
            plt.scatter([1,2,3], [4,5,6])
            plt.title("Some actual stuff")
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(prevent_incorrect_plt(), True)
        self.assertEqual(e.final.message, "You have imported the "
                                    "<code>matplotlib.pyplot</code> module, but you did "
                                    "not rename it to <code>plt</code> using "
                                    "<code>import matplotlib.pyplot as plt</code>.")

        student_code = dedent('''
            import matplotlib.pyplot as plt
            scatter([1,2,3], [4,5,6])
            plt.title("Some actual stuff")
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(prevent_incorrect_plt(), True)
        self.assertEqual(e.final.message, "You have attempted to use the MatPlotLib "
                                    "function named <code>scatter</code>. However, you "
                                    "imported MatPlotLib in a way that does not "
                                    "allow you to use the function directly. I "
                                    "recommend you use <code>plt.scatter</code> instead, "
                                    "after you use <code>import matplotlib.pyplot as "
                                    "plt</code>.")
        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.scatter([1,2,3], [4,5,6])
            plt.title("Some actual stuff")
            plt.show()
        ''')
        with Execution(student_code) as e:
            self.assertEqual(prevent_incorrect_plt(), False)


class TestSignatures(unittest.TestCase):
    def test_function_signature(self):
        student_code = dedent("""
        def find_string(needle, haystack):
            '''
            Finds the given needle in the haystack.

            Args:
                haystack(list[str]): The list of strings to look within.
                needle(str): The given string to be searching for.
                garbage(list[int, tuple[str, bool], or bool], dict[pair[int, int], str], or bool or int): Woah what the heck.
            Returns:
                bool: Whether the string is in the list.
            '''
        """)
        with Execution(student_code) as e:
            self.assertEqual(function_signature(
                "find_string",
                needle="str", haystack="list[str]",
                garbage="dict[pair[int, int], str], list[int, tuple[str, bool], or bool], or bool or int",
                returns="bool"
            ), ([], True))
        bad_code = dedent("""
            def haha_what(something, another):
                '''
                I don't even know man.
                
                It's got some stuff in it.
                
                OH NO I INDENTED.
                
                arguments:
                    something (int or str): This was a things
                        and now it's also indented.
                    another (banana): A cephalopod
                return:
                    int: Something
                    bool: Or else
                '''
        """)
        with Execution(bad_code) as e:
            self.assertEqual(function_signature(
                "haha_what",
                something="str or int", another="banana",
                returns="bool or int"
            ), ([], True))
        
        bad_code = dedent("""
            def bad_function(malformed1, malformed2):
                '''
                Some long description
                
                Args
                malformed1 str Description1
                malformed2 int Description2
                Returns:
                    float: number of pages to fill
                '''
        """)
        with Execution(bad_code) as e:
            signature = function_signature(
                "bad_function",
                malformed1="str", malformed2="int",
                returns="float"
            )
            self.assertEqual(signature[1], True)
            self.assertEqual(set(signature[0]), {"malformed1", "malformed2"})
        
        student_code = dedent("""
        def fixed_function(malformed1, two_part_name):
            '''
            Some long description
            
            Args:
                malformed1 (str): The contents of the book as a string
                two_part_name (int): the letters on each page
            Returns:
                float: number of pages to fill
            '''
        """)
        with Execution(student_code) as e:
            signature = function_signature(
                "fixed_function",
                malformed1="str", two_part_name="int",
                returns="float"
            )
            self.assertEqual(signature[1], True)
            self.assertEqual(signature[0], [])


class TestRecords(unittest.TestCase):
    def test_check_instance_works(self):
        student_code = dedent("""
        banana = {"Name": "Banana", "Age": 47, "Macros": [0, 24, 33]}
        """)
        Fruit = {"Name": str, "Age": int, "Macros": [int]}
        with Execution(student_code) as e:
            result = check_record_instance(e.student.data['banana'], Fruit, "banana", "Fruit")
        self.assertTrue(result)

    def test_check_instance_failed_dict(self):
        student_code = dedent("""
        banana = "Banana"
        """)
        Fruit = {"Name": str, "Age": int, "Macros": [int]}
        with Execution(student_code) as e:
            result = check_record_instance(e.student.data['banana'], Fruit, "`banana`", "Fruit")
        self.assertFalse(result)
        self.assertEqual("`banana` was not a Fruit because it is not a dictionary.", e.final.message)

    def test_check_instance_failed_missing_key(self):
        student_code = dedent("""
        banana = {"Name": "Banana", "Macros": [0, 24, 33]}
        """)
        Fruit = {"Name": str, "Age": int, "Macros": [int]}
        with Execution(student_code) as e:
            result = check_record_instance(e.student.data['banana'], Fruit, "`banana`", "Fruit")
        self.assertFalse(result)
        self.assertEqual("`banana` was supposed to have the key `Age`, but it did not.", e.final.message)


    def test_check_instance_failed_wrong_key_type(self):
        student_code = dedent("""
        banana = {"Name": "Banana", "Age": 'old', "Macros": [0, 24, 33]}
        """)
        Fruit = {"Name": str, "Age": int, "Macros": [int]}
        with Execution(student_code) as e:
            result = check_record_instance(e.student.data['banana'], Fruit, "`banana`", "Fruit")
        self.assertFalse(result)
        self.assertEqual("`banana` was not a Fruit because its key `Age` did not have a `int` value", e.final.message)

    def test_check_instance_failed_extra_keys(self):
        student_code = dedent("""
        banana = {"Name": "Banana", "Age": 4, "Dumb": "Wrong", "Macros": [0, 24, 33]}
        """)
        Fruit = {"Name": str, "Age": int, "Macros": [int]}
        with Execution(student_code) as e:
            result = check_record_instance(e.student.data['banana'], Fruit, "`banana`", "Fruit")
        self.assertFalse(result)
        self.assertEqual("`banana` had extra keys that it should not have.", e.final.message)


if __name__ == '__main__':
    unittest.main(buffer=False)
