"""This file contains helper functions which facilitate data handling in other programs and increase
their readability. """

import json
from math import sqrt

from lightning import LightningRpc, RpcError

from utils.classes import InitInfo


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
    """Displays a basic command line progress bar based on input completion ratio."""
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


def find_in_channels(input_file, node_id):
    """Finds a given node (id) in a list of channels which is stored in a JSON file (input_file). See ln_mapper_gossip.py"""

    channel_results = []
    with open(input_file) as file:
        network_data = json.load(file)
        for channel in network_data['channels']:
            if channel["src"] == node_id or channel["dest"] == node_id:
                channel_results.append(channel)
    if len(channel_results) == 0:
        print(node_id + " not found in list of active channels.")
        return None
    return channel_results


def show_route(rpc_object, src, dest, amount_msat):
    try:
        route = rpc_object.getroute(fromid=src, node_id=dest, msatoshi=amount_msat, riskfactor=0)
        print("Successfully found a route for " + str(amount_msat) + " msat from " + src + " to " + dest + ":")
        print_json(route)
    except RpcError:
        print("Could not find a route from " + src + " to " + dest + "!")


def find_max_amount_for_route(rpc_object, src, dest, sensitivity=2.0):
    amount_msat = 1000
    initial_loop = True

    # Geometric increase
    while initial_loop:
        try:
            test_amount_msat = int(amount_msat * sensitivity)
            route = rpc_object.getroute(fromid=src, node_id=dest, msatoshi=test_amount_msat, riskfactor=0)
            amount_msat = test_amount_msat
        except RpcError as r:
            sensitivity = sqrt(sensitivity)
            if sensitivity == 1:
                initial_loop = False

    # Linear increase
    increment_amount = 1000.0
    while True:
        try:
            test_amount_msat = int(amount_msat + increment_amount)
            route = rpc_object.getroute(fromid=src, node_id=dest, msatoshi=test_amount_msat, riskfactor=0,
                                        fuzzpercent=0)
            amount_msat = test_amount_msat
        except RpcError as r:
            increment_amount = increment_amount / 10
            if increment_amount < 1:
                return int(amount_msat - increment_amount)
