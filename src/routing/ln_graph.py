import argparse
import json
import os

import matplotlib.pyplot as plt

import networkx as nx

parser = argparse.ArgumentParser(
    description="Visualizes.")
parser.add_argument("-g", "--gui-only",
                    action='store_true',
                    help="Only visualizes data specified in provided JSON file (-f).",
                    dest="gui_only")
parser.add_argument("-f", "--input-file",
                    help="Specifies the file from which to load the network information.",
                    default=os.getcwd() + "/network_data.json",
                    dest="input_file")
args = parser.parse_args()

ln_graph = nx.Graph()

if not args.gui_only:
    print("Initialized graphing. Starting LN mapper...")
    os.system('python3 ./ln_mapper.py')

with open(args.input_file, "r") as net_data:
    peer_channel_dict = json.load(net_data)
peer_list = peer_channel_dict["peers"]
channel_list = peer_channel_dict["channels"]
print("Successfully read data from " + args.input_file + ".")

ln_graph.add_nodes_from(peer_list)
nx.draw(ln_graph)
plt.show()
