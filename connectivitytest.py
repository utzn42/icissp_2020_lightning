from lightning import LightningRpc

l5 = LightningRpc("/home/utz/.lightning/lightning-rpc")

info5 = l5.getinfo()
print(info5)

funds = l5.listfunds()
print(funds)
