import argparse
import json

from lightning import LightningRpc

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object", default="/home/utz/.lightning/lightning-rpc",
                    dest="rpc_path")
args = parser.parse_args()


def format_output(raw_data):
    return json.dumps(raw_data, indent=4, sort_keys=True, default=str)


def initialize(rpc_path):
    print("Loading RPC object at: " + rpc_path + "...")
    try:
        temp_rpc_object = LightningRpc(rpc_path)
        print(format_output(temp_rpc_object.getinfo()))
        return temp_rpc_object
    except FileNotFoundError:
        print("Could not load RPC object at " + rpc_path + ".")


rpc_object = initialize(args.rpc_path)
print(format_output(rpc_object.listfunds()))
# print(format_output(rpc_object.listchannels()))
