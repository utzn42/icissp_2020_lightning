import json


class InitInfo:
    def __init__(self, info):
        self.node_id = info["id"]
        self.block_height = info["blockheight"]
        self.network = info["network"]
        self.version = info["version"]


class FundsInfo:
    def __init__(self, funds):
        self.address_funds = {}
        for output in funds["outputs"]:
            if output["address"] in self.address_funds:
                self.address_funds[output["address"]] += output["value"] / 100000000.0
            else:
                self.address_funds[output["address"]] = output["value"] / 100000000.0


class ChannelInfo:

    def __init__(self, peers):
        channels = []
        for peer in peers["peers"]:
            channels += peer["channels"]
        self.count = len(channels)

        self.total_msat = 0
        for channel in channels:
            self.total_msat += channel["msatoshi_total"]


def print_json(raw_data):
    print(json.dumps(raw_data, indent=4, sort_keys=True, default=str))
