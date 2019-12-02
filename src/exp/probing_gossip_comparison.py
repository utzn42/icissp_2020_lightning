"""A file which tests whether probing or gossiping yields faster results for a channel exhausting transaction."""

import argparse

# Retrieve arguments and parse them into variables.
from lightning import RpcError

from util.functions import initialize, print_json

parser = argparse.ArgumentParser(
    description="Tests whether gossiping or probing returns an update in channel balances / routes faster.")
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/lightning-rpc",
                    dest="rpc_path")
args = parser.parse_args()

node_id = "02ce69f8df301a64d4d00a3a9473d040f2e7f86479464b7e1afca78c643fc6dbc1"
amount_msat = 1000

rpc_object = initialize(args.rpc_path)
route = None

try:
    route = rpc_object.getroute(fromid="036e389fce387e10d20ff2d5e1c6f78f530fe030638f6a3e6cfad068799a2ae15f",
                                node_id="0270685ca81a8e4d4d01beec5781f4cc924684072ae52c507f8ebe9daf0caaab7b",
                                msatoshi=amount_msat, riskfactor=0)
    print_json(route)
except RpcError:
    print("Could not find route to node \"" + node_id + "\" !")
