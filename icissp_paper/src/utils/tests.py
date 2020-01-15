import time

from icissp_paper.src.utils.commons import local_rpc_object, default_rpc_object

local_rpc_object.delexpiredinvoice()
pmnt_hash = local_rpc_object.invoice(msatoshi=5000, label="test", description="Initial balance redistribution",
                                     expiry=10)["payment_hash"]
print(pmnt_hash)
time.sleep(2)

default_rpc_object.pay(pmnt_hash)

local_rpc_object.delexpiredinvoice()
default_rpc_object.pay(
    local_rpc_object.invoice(msatoshi=50000000, label="test", description="Initial balance redistribution",
                             expiry=5)["payment_hash"])
