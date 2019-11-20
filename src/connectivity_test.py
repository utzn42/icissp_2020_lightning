"""A script which connects to a lightning RPC object, and then prints some basic information along with the addresses
and the corresponding balances as well as a summary of connected peers and channels. """

import argparse

from util.classes import FundsInfo, ChannelInfo
# Parse command line arguments.
from util.functions import initialize

parser = argparse.ArgumentParser(
    description="Tests the connection of a local Lightning RPC objects and displays some basic information.")
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/lightning-rpc",
                    dest="rpc_path")
args = parser.parse_args()


def print_address_balances(funds: dict):
    """Takes in a dictionary returned by LightningRpc.listfunds() and prints addresses and corresponding funds for the
    current instance. """

    local_funds = FundsInfo(funds)
    print("Addresses / Funds (BTC):")
    print(local_funds.address_funds, end="\n \n")


def print_channel_info(peers: dict):
    """Takes in a dictionary returned by LightningRpc.listpeers() and displays an executive summary on the amount of
    connections as well as the amount of BTC within active channels. """

    channel_info = ChannelInfo(peers)
    print("Currently connected to " + str(len(peers.keys())) + " peer(s) over " + str(
        channel_info.count) + " channel(s).")
    print("Total BTC count: " + str(channel_info.total_btc) + "\n")


# Main program sequence starts here:
rpc_object = initialize(args.rpc_path)
print_address_balances(rpc_object.listfunds())
print_channel_info(rpc_object.listpeers())
print("Successfully connected to local Lightning daemon!")
