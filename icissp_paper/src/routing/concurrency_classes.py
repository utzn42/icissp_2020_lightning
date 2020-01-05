from threading import *


class Probe(Thread):

    def __init__(self, rpc_object, channel):
        super(Probe, self).__init__()
        self.rpc_object = rpc_object
        self.channel = channel

    def run(self):
        print(self.rpc_object.getinfo())


class ReverseProbe(Thread):

    def __init__(self, rpc_object, channel):
        super(ReverseProbe, self).__init__()
        self.rpc_object = rpc_object
        self.channel = channel

    def run(self):
        print(self.rpc_object.getinfo())
