import re
import inspect
import utils


"""
The takout from this should be
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
        # all of the \s* is for multiply spaces to execute
        contents = re.sub(
            r'\{%\s*if\s*(.*?)\s*%\}(.*?)(?:\{%\s*else if\s*(.*?)\s*%\}(.*?))*(?:\{%\s*else\s*%\}(.*?))?\{%\s*endif\s*%\}',
            lambda match: self.__process_conditionals(match),
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

    def __execute_expression(self, match) -> str:
        for line in match.group(1).split('\n'):
            line = line.strip().replace("self.__", "self._Analyzer__")
            exec(line, self.target_members)
        return self.REMOVEME_SYNTAX

    def __process_conditionals(self, match) -> str:
        conditions = match.groups()[::2]            # Wont explain what the :: does, play with it!
        contents = match.groups()[1::2]             # Same for this

        for condition, content in zip(conditions, contents):
            if condition and eval(condition.strip(), self.target_members):
                return content.strip()

        return contents[-1].strip() if contents[-1] else ""

    def __evaluate_expression(self, match) -> str:
        expr = match.group(1).strip().replace("self.__", "self._Analyzer__")
        return str(eval(expr, self.target_members))


def getmembers(object: object, extras: dict={}, extras_name: str = "params"):
    """
    For the object parameter pass "self".
    For the extras parameter, if requested, pass a dict of the requested items.
    If the extras paramater should be a function parameter, pass "locals()"
    """

    return utils.appendd({
        name : value for name, value in inspect.getmembers_static(object)
    }, {extras_name: extras} )
