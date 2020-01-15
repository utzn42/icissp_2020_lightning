from lightning import RpcError

from icissp_paper.src.utils.commons import local_rpc_object, default_rpc_object

# Connect n3 to n1
try:
    local_rpc_object.connect(peer_id="03bdc681dae47766db11c9c991ba217e28ae1a0d0066199630b1a9b33258541415",
                             host="192.168.0.59", port=9735)
except RpcError as e:
    print("Local node could not connect to default node.")
    print(e)

# Open a channel from n1 to n3
default_rpc_object.fundchannel(node_id="03e95039d51c79e9b07115b928e29b2d39f4a568a7223175b092866620efd78b21",
                               satoshi=200000)

# Redistribute funds 50-50 between n1 and n3
local_rpc_object.delexpiredinvoice()
default_rpc_object.pay(
    local_rpc_object.invoice(msatoshi=100000000, label="test", description="Initial balance redistribution",
                             expiry=5)["payment_hash"])

# Connect n1 to n2
try:
    default_rpc_object.connect(peer_id="0331f6d8f3b32ffceae2400ce9ff7da9e5501f02e74cba996d830d4c5430c2e9d6",
                               host="192.168.0.60", port=9735)
except RpcError as e:
    print("Local node could not connect to default node.")
    print(e)

# Open a channel from n1 to n2
default_rpc_object.fundchannel(node_id="0331f6d8f3b32ffceae2400ce9ff7da9e5501f02e74cba996d830d4c5430c2e9d6",
                               satoshi=200000)
