from lightning import LightningRpc

l1 = LightningRpc("/tmp/")

# Traceback (most recent call last):
# File "/home/utz/Desktop/ba-code/ba-nisslmueller/connectivitytest.py", line 14, in <module>
#  info1 = l1.getinfo()
# File "/home/utz/Desktop/lightning/contrib/pylightning/lightning/lightning.py", line 606, in getinfo
#  return self.call("getinfo")
# File "/home/utz/Desktop/lightning/contrib/pylightning/lightning/lightning.py", line 221, in call
#  sock.connect(self.socket_path)
# ConnectionRefusedError: [Errno 111] Connection refused

info1 = l1.getinfo()
print(info1)