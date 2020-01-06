import random
import string
import time

from lightning import RpcError


class Probe():

    def __init__(self, rpc_object, channel):
        super(Probe, self).__init__()
        self.rpc_object = rpc_object
        self.channel = channel
        self.payment_hash = None
        self.params = None
        self.route = None

    def probe(self, msat):
        self.payment_hash = ''.join(random.choice(string.hexdigits) for _ in range(64))
        self.params = {
            "node_id": "028020f074310d236c80a581f5f065f24463388e8f0eca713b90a6ad95a2c9b7c0",
            "msatoshi": int(msat),
            "riskfactor": 1
        }
        self.route = self.rpc_object.getroute(**self.params)["route"]
        try:
            self.rpc_object.sendpay(self.route, self.payment_hash)
            self.rpc_object.waitsendpay(self.payment_hash)
            print("Uh-oh. Guessed payment hash correctly: " + self.payment_hash)
            return
        except RpcError as e:
            return e.error["code"]

    def find_init_max(self):
        min_msat = 0
        max_msat = self.channel["amount_msat"].millisatoshis
        amount_msat = int(self.channel["amount_msat"].millisatoshis / 2)
        while True:
            error = self.probe(amount_msat)
            if error == 203:
                min_msat = amount_msat
            if error == 204:
                max_msat = amount_msat
            if error == 205:
                print("No suitable route found. Check connection.")
                return None
            if max_msat - min_msat < 1000:
                return amount_msat
            amount_msat = int((min_msat + max_msat) / 2)

    def monitor_balance(self, init_max):
        new_max = init_max
        while True:
            time.sleep(5)
            if self.probe(init_max) == 204:
                print("Monitor: Channel balance has decreased from " + str(init_max))
                print("Monitor: Calculating new balance...", end="")
                new_max = self.find_init_max()
                print(new_max, ", delta: " + str(new_max - init_max))
            time.sleep(5)
            if self.probe(init_max + 1000) == 203:
                print("Monitor: Channel balance has increased from " + str(init_max))
                print("Monitor: Calculating new balance...", end="")
                new_max = self.find_init_max()
                print(new_max, ", delta: " + str(new_max - init_max))
            init_max = new_max

    def run(self):
        print("Probe: Finding initial maximum balance...")
        init_max = self.find_init_max()
        print("Probe: Initial maximum balance found: " + str(init_max))
        print("Probe: Monitoring for changes...")
        self.monitor_balance(init_max)
