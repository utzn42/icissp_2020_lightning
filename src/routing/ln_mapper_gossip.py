import argparse
import json
import os

from utils.classes import Channel
from utils.functions import initialize, delete_file_content

# Retrieve arguments and parse them into variables.
parser = argparse.ArgumentParser(
    description="Constructs a local view of all currently active LN nodes and channels.")
parser.add_argument("-r", "--rpc-file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/testnet/lightning-rpc",
                    dest="rpc_path")
parser.add_argument("-o", "--output",
                    help="path of the JSON output file",
                    default=os.getcwd() + "/network_data.json",
                    dest="output_file")
args = parser.parse_args()

# Initialize RPC object and query local nodes' known channels.
local_rpc_object = initialize(args.rpc_path)


def map_ln(rpc_object=initialize("/home/kynes/.lightning/testnet/lightning-rpc"), output_file="/network_data.json"):
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

    # Write results to JSON file which was specified in parameters. Default: ../network_data.json
    print("Copying peer & channel list to " + args.output_file)
    json_dict = {"peers": peer_list, "channels": channel_list}
    with open(args.output_file, "at") as write_file:
        json.dump(json_dict, write_file)


map_ln(local_rpc_object, args.output_file)
