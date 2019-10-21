import json

import blockcypher

data = json.dumps(blockcypher.get_blockchain_overview("btc-testnet"), indent=4, sort_keys=True, default=str)
print(data)
