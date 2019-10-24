import json


def print_json(raw_data):
    print(json.dumps(raw_data, indent=4, sort_keys=True, default=str))
