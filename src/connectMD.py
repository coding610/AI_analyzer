import re
import inspect
import utils


"""
The learning from this should be
that regex is really awesome
"""

class MDConnection:
    def __init__(self, target_class: object, target_members: dict, read_file: str, write_file: str, connect: bool = False) -> None:
        self.REMOVEME_SYNTAX = "{[{!REMOVEME!}]}"

        self.target_class: object = target_class
        self.target_members: dict = target_members
        self.read_file: str = read_file 
        self.write_file: str = write_file

        self.target_members["self"] = self.target_class

        if connect: self.connect()

    def connect(self) -> str | None:
        with open(self.read_file, "r") as f:
            contents = f.read()

        contents = self.__replace_expressions(contents)

        with open(self.write_file, "w") as f:
            f.write(contents)

    def __replace_expressions(self, contents: str) -> str:
        contents = self.__apply_macros(contents)

        # all of the \s* is for multiply spaces to execute
        contents = re.sub(
        	r'\{%\s*if\s*(.*?)\s*%\}(.*?)(?:\{%\s*else\s*%\}(.*?))?\{%\s*endif\s*%\}',
            lambda match: self.__process_conditional(match),
            contents,
            flags=re.DOTALL
        )
        contents = re.sub(
            r'\{\<(.*?)\>\}',
            lambda match: self.__execute_expression(match),
            contents,
            flags=re.DOTALL
        )
        contents = re.sub(
            r'\{\{(.*?)\}\}',
            lambda match: self.__evaluate_expression(match),
            contents,
            flags=re.DOTALL
        )

        return contents.replace(self.REMOVEME_SYNTAX + "\n", "").replace(self.REMOVEME_SYNTAX, "")

    def __apply_macros(self, contents: str) -> str:
        return contents.replace("self.__", "self._Analyzer__")

    def __process_conditional(self, match) -> str:
        # [0] -> if statement
        # [1] -> if body
        # [2] -> else body

        if match.groups()[0] != None and self.__eval(match.groups()[0]):
            return match.groups()[1].strip()
        elif match.groups()[2] != None:
            return match.groups()[2].strip()
        else:
            return ""

    def __execute_expression(self, match) -> str:
        for line in match.group(1).split('\n'):
            self.__exec(line.strip())
        return self.REMOVEME_SYNTAX

    def __evaluate_expression(self, match) -> str:
        return self.__eval(match.group(1).strip())

    def __eval(self, expression) -> str:
        # TODO: Error Handleling
        return str(eval(expression, self.target_members))

    def __exec(self, expression):
        # TODO: Error Handleling
        exec(expression, self.target_members)

def getmembers(object: object, extras: dict={}, extras_name: str = "params"):
    """
    For the object parameter pass "self".
    For the extras parameter, if requested, pass a dict of the requested items.
    If the extras paramater should be a function parameter, pass "locals()"
    """

    return utils.appendd({
        name : value for name, value in inspect.getmembers_static(object)
    }, {extras_name: extras} )

def wrapn(i: int) -> int:
    return 9999999 if i == -1 else i
