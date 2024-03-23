import sys
import json

def dprint(d: dict) -> None:
    print(json.dumps(d, indent=4, default=str))

def appendd(d1: dict, d2: dict) -> dict:
    d1.update(d2)
    return d1

def replace_by_index(string: str, replacement: str, index: int) -> str:
    return string[:index-1] + replacement

def err(mess: str) -> None:
    print(mess)
    sys.exit()
