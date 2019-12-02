"""A file which tests whether probing or gossiping yields faster results for a channel exhausting transaction."""

import argparse

from utils.functions import initialize, show_route

# Retrieve arguments and parse them into variables.
parser = argparse.ArgumentParser(
    description="Tests whether gossiping or probing returns an update in channel balances / routes faster.")
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/testnet/lightning-rpc",
                    dest="rpc_path")
parser.add_argument("-s", "--src",
                    help="Source node ID",
                    default="036e389fce387e10d20ff2d5e1c6f78f530fe030638f6a3e6cfad068799a2ae15f",
                    dest="src_id")
parser.add_argument("-d", "--dest",
                    help="destination node ID",
                    default="02ce69f8df301a64d4d00a3a9473d040f2e7f86479464b7e1afca78c643fc6dbc1",
                    dest="dest_id")
parser.add_argument("-a", "--amount",
                    help="amount to send in millisatoshi",
                    default=1000,
                    dest="amount_msat")
args = parser.parse_args()

rpc_object = initialize(args.rpc_path)

# Probe for route between src_id and dest_id
show_route(rpc_object, args.src_id, args.dest_id, args.amount_msat)
