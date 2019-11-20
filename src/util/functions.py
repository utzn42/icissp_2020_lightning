"""This file contains helper functions which facilitate data handling in other programs and increase
their readability. """

import json
from lightning import LightningRpc

from util.classes import InitInfo


def print_json(raw_data):
    """Prints a JSON object, and parses unknown data types into strings."""

    print(json.dumps(raw_data, indent=4, sort_keys=True, default=str))


def initialize(rpc_path: str) -> LightningRpc:
    """"Takes the path of the RPC file as a parameter and runs getinfo(). If successful, some basic information is
    printed, and an RPC object is returned for further use. If not, an error is raised, informing the user of an
    incorrect file path. """

    print("Loading RPC object at: " + rpc_path + "..." + "\n")
    try:
        temp_rpc_object = LightningRpc(rpc_path)
        info = InitInfo(temp_rpc_object.getinfo())
        print("Node ID: " + info.node_id + "\n" + "Block height: " + str(
            info.block_height) + " (" + info.network + ")" + "\n"
              + "Version: " + info.version + "\n")
        return temp_rpc_object
    except FileNotFoundError:
        print("Could not load RPC object at " + rpc_path + "." + "\n")


def delete_file_content(file):
    """Empties a file specified by the file parameter."""
    with open(file, "w"):
        pass


def display_progress_bar(ratio):
    if ratio > 0.9:
        print("90%...")
        return 0.9
    if ratio > 0.8:
        print("80%...", end="")
        return 0.8
    if ratio > 0.7:
        print("70%...", end="")
        return 0.7
    if ratio > 0.6:
        print("60%...", end="")
        return 0.6
    if ratio > 0.5:
        print("50%...", end="")
        return 0.5
    if ratio > 0.4:
        print("40%...", end="")
        return 0.4
    if ratio > 0.3:
        print("30%...", end="")
        return 0.3
    if ratio > 0.2:
        print("20%...", end="")
        return 0.2
    if ratio > 0.1:
        print("10%...", end="")
        return 0.1
    print("0%...", end="")
    return 0.0

