import sys
import json

from sklearn.metrics import r2_score
import numpy as np

def dprint(d: dict) -> None:
    print(json.dumps(d, indent=4, default=str))

def dmerge(d1: dict, d2: dict):
    return {**d1, **d2}

def appendd(d1: dict, d2: dict) -> dict:
    d1.update(d2)
    return d1

def replace_by_index(string: str, replacement: str, index: int) -> str:
    return string[:index-1] + replacement

def err(mess: str) -> None:
    print(mess)
    sys.exit()

def r2score(y_true, y_pred) -> np.float64 | None:
    s = r2_score(y_true, y_pred)
    if type(s) == np.float64:
        return s
    else:
        return None
