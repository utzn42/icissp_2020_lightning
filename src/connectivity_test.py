import argparse

import help_utils as utils
from lightning import LightningRpc

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object", default="/home/utz/.lightning/lightning-rpc",
                    dest="rpc_path")
args = parser.parse_args()


def initialize(rpc_path):
    print("Loading RPC object at: " + rpc_path + "..." + "\n")
    try:
        temp_rpc_object = LightningRpc(rpc_path)
        info = utils.InitInfo(temp_rpc_object.getinfo())
        print("Node ID: " + info.node_id + "\n" + "Block height: " + str(
            info.block_height) + " (" + info.network + ")" + "\n"
              + "Version: " + info.version + "\n")
        return temp_rpc_object
    except FileNotFoundError:
        print("Could not load RPC object at " + rpc_path + "." + "\n")


def print_address_balances(funds):
    funds = utils.FundsInfo(funds)
    print("Addresses / Funds (BTC):")
    print(funds.address_funds, end="\n \n")


def print_channel_info(peers):
    channel_info = utils.ChannelInfo(peers)
    print("Currently connected to " + str(len(peers.keys())) + " peer(s) over " + str(
        channel_info.count) + " channel(s).")
    print("Total BTC count: " + str(channel_info.total_msat / 100000000000.0) + "\n")


rpc_object = initialize(args.rpc_path)
print_address_balances(rpc_object.listfunds())
print_channel_info(rpc_object.listpeers())
print("Successfully connected to local Lightning daemon!")
