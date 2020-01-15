from lightning import LightningRpc

local_path = "/home/kynes/.lightning/local_node/testnet/lightning-rpc"
default_path = "/home/kynes/.lightning/testnet/lightning-rpc"


# Initialize RPC object
def initialize(rpc_path):
    try:
        temp_rpc_object = LightningRpc(rpc_path)
        return temp_rpc_object
    except FileNotFoundError:
        print("Could not load RPC object at " + rpc_path + "." + "\n")


local_rpc_object = initialize(local_path)
default_rpc_object = initialize(default_path)
