import argparse

from lightning import LightningRpc

from icissp_paper.src.routing.concurrency_classes import *

parser = argparse.ArgumentParser(description="Probing Attack")
parser.add_argument("-r", "--rpc-file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/local_node/testnet/lightning-rpc",
                    dest="rpc_path")
parser.add_argument("-c", "--channel",
                    help="short channel ID of the channel to be monitored",
                    default="1638564x67x0",
                    dest="target_channel")
args = parser.parse_args()


# Initialize RPC object
def initialize(rpc_path):
    try:
        temp_rpc_object = LightningRpc(rpc_path)
        return temp_rpc_object
    except FileNotFoundError:
        print("Could not load RPC object at " + rpc_path + "." + "\n")


# Find total balance for targeted channel from gossip_store
def find_channel_by_short_id():
    for target_channel in local_rpc_object.listchannels()["channels"]:
        if target_channel["short_channel_id"] == args.target_channel:
            return target_channel


local_rpc_object = initialize(args.rpc_path)

channel = find_channel_by_short_id()

p = Probe(local_rpc_object, channel)
p.run()
