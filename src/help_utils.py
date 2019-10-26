"""This file contains helper classes and functions which facilitate data handling in other programs and increase
their readability. """

import json


class InitInfo:
    """Takes in a getinfo() return object and stores the node ID, block height, operating chain and protocol version
    for further use. """

    def __init__(self, info: dict):
        self.node_id = info["id"]
        self.block_height = info["blockheight"]
        self.network = info["network"]
        self.version = info["version"]


class FundsInfo:
    """Takes in a listfunds() return object and keeps a dictionary of found addresses and their corresponding
    balances. """

    def __init__(self, funds: dict):
        self.address_funds = {}

        for output in funds["outputs"]:

            # If the address already exists within the dictionary, append the output value to the existing balance.
            if output["address"] in self.address_funds:

                # Divide by 100000000 to convert Millisatoshi to BTC.
                self.address_funds[output["address"]] += output["value"] / 100000000

            # If the address does not exist, create a new entry for the address and store the corresponding balance.
            else:

                # Divide by 100000000 to convert Millisatoshi to BTC.
                self.address_funds[output["address"]] = output["value"] / 100000000


class ChannelInfo:
    """Takes in a listpeers() return objects and counts the amount of active peers and channels. It then calculates
    the total amount of BTC locked within these channels. """

    def __init__(self, peers: dict):

        # Count peers and channels.
        channels = []
        for peer in peers["peers"]:
            channels += peer["channels"]
        self.count = len(channels)

        # Calculate BTC amount within channels.
        self.total_btc = 0
        for channel in channels:
            # Divide by 100000000 to convert Millisatoshi to BTC.
            self.total_btc += channel["msatoshi_total"] / 100000000


def print_json(raw_data):
    """Prints a JSON object, and parses unknown data types into strings."""

    print(json.dumps(raw_data, indent=4, sort_keys=True, default=str))
