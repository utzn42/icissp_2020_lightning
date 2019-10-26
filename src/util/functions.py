"""This file contains helper functions which facilitate data handling in other programs and increase
their readability. """

import json


def print_json(raw_data):
    """Prints a JSON object, and parses unknown data types into strings."""

    print(json.dumps(raw_data, indent=4, sort_keys=True, default=str))
