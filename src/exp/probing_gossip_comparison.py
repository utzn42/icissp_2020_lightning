"""A file which tests whether probing or gossiping yields faster results for a channel exhausting transaction."""

import argparse

from utils.functions import initialize, show_route, find_max_amount_for_route

# Retrieve arguments and parse them into variables.
parser = argparse.ArgumentParser(
    description="Tests whether gossiping or probing returns an update in channel balances / routes faster.")
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/testnet/lightning-rpc",
                    dest="rpc_path")
parser.add_argument("-s", "--src",
                    help="Source node ID",
                    default="039d813433a915263fe53cad421057e4d3e3467c46f9690e239283a4b10b280e6d",
                    dest="src_id")
parser.add_argument("-d", "--dest",
                    help="destination node ID",
                    default="028020f074310d236c80a581f5f065f24463388e8f0eca713b90a6ad95a2c9b7c0",
                    dest="dest_id")
parser.add_argument("-a", "--amount",
                    help="amount to send in millisatoshi",
                    default=99999900,
                    dest="amount_msat")
args = parser.parse_args()

rpc_object = initialize(args.rpc_path)

# Probe for route between src_id and dest_id
show_route(rpc_object, args.src_id, args.dest_id, args.amount_msat)
print(find_max_amount_for_route(rpc_object, args.src_id, args.dest_id))
