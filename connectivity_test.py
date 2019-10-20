import argparse

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
        print(temp_rpc_object.getinfo())
        return temp_rpc_object
    except FileNotFoundError:
        print("Could not load RPC object at " + rpc_path + ".")


rpc_object = initialize(args.rpc_path)
