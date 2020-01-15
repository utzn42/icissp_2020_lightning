from icissp_paper.src.utils.commons import local_rpc_object

# Close channel and reconnect to signal cooperation
local_rpc_object.close("03bdc681dae47766db11c9c991ba217e28ae1a0d0066199630b1a9b33258541415")
local_rpc_object.connect(peer_id="03bdc681dae47766db11c9c991ba217e28ae1a0d0066199630b1a9b33258541415",
                         host="192.168.0.59", port=9735)
