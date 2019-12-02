import argparse
import json
import os

from lightning import RpcError

from utils.classes import Channel
from utils.functions import initialize, delete_file_content, print_json, display_progress_bar

# Retrieve arguments and parse them into variables.
parser = argparse.ArgumentParser(
    description="Constructs a local view of all currently active LN nodes and channels.")
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/testnet/lightning-rpc",
                    dest="rpc_path")
parser.add_argument("-o", "--output",
                    help="path of the JSON output file",
                    default=os.getcwd() + "/network_data.json",
                    dest="output_file")
parser.add_argument("-p", "--probing-level",
                    help="specifies whether and how extensively to look for active, unannounced channels (max=5)",
                    default=0,
                    dest="probing_level")
args = parser.parse_args()

# Initialize RPC object and query local nodes' known channels.
rpc_object = initialize(args.rpc_path)
print("Retrieving channel gossip information...")
peer_channels = rpc_object.listchannels()
# print_json(peer_channels)

# Flush output file, in case of previously run test still being present.
delete_file_content(args.output_file)

# Set up storage lists & variables for parsing loop
print("Parsing peers & channels...")
peer_list = []
channel_list = []
active_channel_count = 0

# Parsing loop. Add unseen peers to peer list and every channel to channel list.
for channel in peer_channels["channels"]:
    if channel["source"] not in peer_list:
        peer_list.append(channel["source"])
    if channel["destination"] not in peer_list:
        peer_list.append(channel["destination"])
    if channel["active"]:
        active_channel_count += 1

    channel_list.append(Channel(channel).__dict__)

# Print short overview of results.
print("Found " + str(len(peer_list)) + " active peers and " + str(
    len(channel_list)) + " channels (" + str(
    round((active_channel_count / len(channel_list)) * 100,
          2)) + "% of which are active) based on initial channel gossip.")

if args.probing_level > 0:

    #
    def add_channel_and_node_if_new(route):
        """Helper function for probing loop. Adds nodes and channels appearing in a route to the peer_list if they
        aren't known yet. """
        for node in route["route"]:
            if node["id"] not in peer_list and node["id"] not in peer_list:  # Issue #9.
                peer_list.append(node["id"])


    # Administrative variables for probing loop.
    route_failure_counter = 0
    print_var = 0.0

    # Loop for probing routes to known peers.
    for idx, peer in enumerate(peer_list):
        try:
            add_channel_and_node_if_new(rpc_object.getroute(peer, 1000, riskfactor=0, fuzzpercent=0))
            add_channel_and_node_if_new(rpc_object.getroute(peer, 1000, riskfactor=0, fuzzpercent=50))
            add_channel_and_node_if_new(rpc_object.getroute(peer, 1000, riskfactor=0, fuzzpercent=100))
            add_channel_and_node_if_new(rpc_object.getroute(peer, 1000000, riskfactor=0, fuzzpercent=0))
            add_channel_and_node_if_new(rpc_object.getroute(peer, 1000000, riskfactor=0, fuzzpercent=50))
            add_channel_and_node_if_new(rpc_object.getroute(peer, 1000000, riskfactor=0, fuzzpercent=100))

            if idx / len(peer_list) - print_var > 0.1:
                print_var = display_progress_bar(idx / len(peer_list))
        except RpcError:
            route_failure_counter += 1

# Write results to JSON file which was specified in parameters. Default: ../network_data.json
print("Copying peer & channel list to " + args.output_file)
json_dict = {"peers": peer_list, "channels": channel_list}
with open(args.output_file, "at") as write_file:
    json.dump(json_dict, write_file)
