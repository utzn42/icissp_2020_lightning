"""A script which connects to a lightning RPC object, and then prints some basic information along with the addresses
and the corresponding balances as well as a summary of connected peers and channels. """

import argparse

from lightning import LightningRpc

import help_utils as utils

# Parse command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object", default="/home/utz/.lightning/lightning-rpc",
                    dest="rpc_path")
args = parser.parse_args()


def initialize(rpc_path: str) -> LightningRpc:
    """"Takes the path of the RPC file as a parameter and runs getinfo(). If successful, some basic information is
    printed, and an RPC object is returned for further use. If not, an error is raised, informing the user of an
    incorrect file path. """

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


def print_address_balances(funds: dict):
    """Takes in a dictionary returned by LightningRpc.listfunds() and prints addresses and corresponding funds for the
    current instance. """

    local_funds = utils.FundsInfo(funds)
    print("Addresses / Funds (BTC):")
    print(local_funds.address_funds, end="\n \n")


def print_channel_info(peers: dict):
    """Takes in a dictionary returned by LightningRpc.listpeers() and displays an executive summary on the amount of
    connections as well as the amount of BTC within active channels. """

    channel_info = utils.ChannelInfo(peers)
    print("Currently connected to " + str(len(peers.keys())) + " peer(s) over " + str(
        channel_info.count) + " channel(s).")
    print("Total BTC count: " + str(channel_info.total_btc) + "\n")


# Main program sequence starts here:
rpc_object = initialize(args.rpc_path)
print_address_balances(rpc_object.listfunds())
print_channel_info(rpc_object.listpeers())
print("Successfully connected to local Lightning daemon!")
