import json

def dprint(d: dict):
    print(json.dumps(d, indent=4, default=str))
