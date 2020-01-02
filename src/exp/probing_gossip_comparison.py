"""A file which tests whether probing or gossiping yields faster results for a channel exhausting transaction."""

import argparse
import timeit

from lightning import RpcError

from utils.functions import initialize, find_max_amount_for_route

# Retrieve arguments and parse them into variables.
parser = argparse.ArgumentParser(
    description="Tests whether gossiping or probing returns an update in channel balances / routes faster.")
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/local_node/testnet/lightning-rpc",
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
                    default=1000,
                    dest="amount_msat")
parser.add_argument("-b", "--bolt11",
                    help="BOLT 11 to pay",
                    dest="bolt11")
args = parser.parse_args()

rpc_object = initialize(args.rpc_path)

max_sat = find_max_amount_for_route(rpc_object, args.src_id, args.dest_id)
max_sat_half = int(max_sat / 2)

route_before = None
route_after = None

loop = True

try:
    route_before = rpc_object.getroute(node_id=args.dest_id, msatoshi=max_sat, riskfactor=0)
except RpcError as r:
    print(r)

rpc_object.pay(args.bolt11)
start = timeit.default_timer()
while loop:
    try:
        route_after = rpc_object.getroute(node_id=args.dest_id, msatoshi=max_sat_half, riskfactor=0)
    except RpcError as r:
        stop = timeit.default_timer()
        loop = False
        print(r)
        print('Time it took for routing to fail: ', stop - start)
