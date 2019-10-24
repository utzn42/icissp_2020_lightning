import argparse

from help_utils import print_json
from lightning import LightningRpc

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object", default="/home/utz/.lightning/lightning-rpc",
                    dest="rpc_path")
args = parser.parse_args()


def initialize(rpc_path):
    print("Loading RPC object at: " + rpc_path + "...")
    try:
        temp_rpc_object = LightningRpc(rpc_path)
        print_json(temp_rpc_object.getinfo())
        return temp_rpc_object
    except FileNotFoundError:
        print("Could not load RPC object at " + rpc_path + ".")


def print_address_balances(funds):
    addresses = {}
    for output in funds["outputs"]:
        if output["address"] in addresses:
            addresses[output["address"]] += output["amount_msat"]
        else:
            addresses[output["address"]] = output["amount_msat"]
    print("\n" + "Addresses / Funds:")
    print(addresses)


# TODO: List channels

rpc_object = initialize(args.rpc_path)
print_address_balances(rpc_object.listfunds())
print("\n" + "Successfully connected to local Lightning daemon!")
