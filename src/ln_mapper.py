import argparse
import json

from util.functions import initialize, delete_file_content, display_progress_bar

# Retrieve arguments and parse them into variables.
parser = argparse.ArgumentParser(
    description="Tests the connection of a local Lightning RPC objects and displays some basic information.")
parser.add_argument("-f", "--file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/lightning-rpc",
                    dest="rpc_path")
parser.add_argument("-o", "--output",
                    help="file path of the JSON output file",
                    default="../",
                    dest="output_path")
parser.add_argument("-n", "--output-name",
                    help="file name of the JSON output file",
                    default="network_data.json",
                    dest="output_name")
args = parser.parse_args()

# Initialize RPC object and query local nodes' known channels.
rpc_object = initialize(args.rpc_path)
print("Retrieving channel gossip information...")
peer_channels = rpc_object.listchannels()

# Loop through channel sources and destinations and add them to node pool.
gossip_peer_list = []
for channel in peer_channels["channels"]:
    if channel["source"] not in gossip_peer_list:
        gossip_peer_list.append(channel["source"])
    if channel["destination"] not in gossip_peer_list:
        gossip_peer_list.append(channel["destination"])

# Flush output file, in case of previously run test still being present.
delete_file_content(args.output_name)

print("Found " + str(len(gossip_peer_list)) + " peers based on initial channel gossip. Starting probing...")

# Set up maintenance variables for probing loop.
probing_peer_list = []
route_failure_counter = 0
iterations = 0
print_var = display_progress_bar(0.0)


# Helper function for probing loop. Adds nodes appearing in a route to list if they aren't known yet.
def add_route_node_to_list(route):
    for node in route["route"]:
        if node["id"] not in probing_peer_list and node["id"] not in gossip_peer_list:
            probing_peer_list.append(node["id"])


# Loop for probing routes to known peers. TODO: Add program argument to determine how aggressive probing should be.
for peer in gossip_peer_list:
    iterations += 1
    try:
        add_route_node_to_list(rpc_object.getroute(peer, 1000, riskfactor=0, fuzzpercent=0))
        add_route_node_to_list(rpc_object.getroute(peer, 1000, riskfactor=0, fuzzpercent=50))
        add_route_node_to_list(rpc_object.getroute(peer, 1000, riskfactor=0, fuzzpercent=100))
        add_route_node_to_list(rpc_object.getroute(peer, 1000000, riskfactor=0, fuzzpercent=0))
        add_route_node_to_list(rpc_object.getroute(peer, 1000000, riskfactor=0, fuzzpercent=50))
        add_route_node_to_list(rpc_object.getroute(peer, 1000000, riskfactor=0, fuzzpercent=100))

        if iterations / len(gossip_peer_list) - print_var > 0.1:
            print_var = display_progress_bar(iterations / len(gossip_peer_list))
    except:
        route_failure_counter += 1

peer_dict = {"gossip_peers": gossip_peer_list, "probing_peers": probing_peer_list}
with open("network_data.json", "at") as write_file:
    json.dump(peer_dict, write_file)

print("Found " + str(len(probing_peer_list)) + " additional peers during probing. Total peers: " + str(
    len(gossip_peer_list) + len(probing_peer_list)))
print("Successfully established " + str(
    round((1 - route_failure_counter / iterations) * 100, 2)) + "% of all possible routes.")
