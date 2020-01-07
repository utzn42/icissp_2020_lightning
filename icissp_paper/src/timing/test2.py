import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Timing Attack")
parser.add_argument("-r", "--rpc-file",
                    help="file path of the callable RPC object",
                    default="/home/kynes/.lightning/local_node/testnet/lightning-rpc",
                    dest="rpc_path")
parser.add_argument("-f", "--log-file",
                    help="log file to scan for HTLCs",
                    default="/home/kynes/lnlog.txt",
                    dest="log_path")
parser.add_argument("-t", "--target",
                    help="target node ID for which to listen",
                    default="0282dd07075222684474650af05772bd3298ff1c124c419252888e85d905317f6a",
                    dest="target_id")
args = parser.parse_args()

if not os.path.exists(args.log_path):
    sys.exit("Log file " + args.log_path + " not found. Check parameters.")

with open(args.log_path, "r") as log:
    data = log.readlines()

add_lines = []
fulfill_lines = []

for line in data:
    if line.find("WIRE_UPDATE_ADD_HTLC") > 0 and line.find(args.target_id) > 0:
        add_lines.append(line)
    if line.find("WIRE_UPDATE_FULFILL_HTLC") > 0 and line.find(args.target_id) > 0:
        fulfill_lines.append(line)

for line in add_lines:
    print(line, end="")

print("------------------------")

for line in fulfill_lines:
    print(line, end="")

# print(data)
