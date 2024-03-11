import re
import inspect
from utils import *



class MDConnection:
    def __init__(self, target_class: object, target_members: dict, read_file: str, write_file: str, connect: bool = False) -> None:
        self.target_class: object = target_class
        self.target_members: dict = target_members
        self.read_file: str = read_file 
        self.write_file: str = write_file

        self.target_members["self"] = self.target_class # Add for 

        if connect: self.connect()

    def connect(self) -> str | None:
        with open(self.read_file, "r") as f:
            contents = f.read()

        contents = self.__replace_expressions(contents)

        with open(self.write_file, "w") as f:
            f.write(contents)

    def __replace_expressions(self, contents: str) -> str:
        return re.sub(
            r'\{\{(.*?)\}\}',
            lambda match: self.__evaluate_expression(match),
            contents
        )

    def __evaluate_expression(self, match) -> str:
        expr = match.group(1).strip()

        expr = expr.replace("self.__", "self._Analyzer__")
        return str(eval(expr, self.target_members))

def getmembers(object: object):
    return {
        name : value for name, value in inspect.getmembers_static(object)
    }
