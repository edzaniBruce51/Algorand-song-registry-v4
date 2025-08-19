from algosdk.v2client import algod

# TestNet connection
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""  # No token needed for public nodes.

# Create client
algod_client = algod.AlgodClient(algod_token, algod_address)

try:
    # Test connection
    status = algod_client.status()
    print(f"Connected to Algorand TestNet!")
    print(f"Last round: {status['last-round']}")
    print(f"Network: {status['network']}")
except Exception as e:
    print(f"Connection failed: {e}")