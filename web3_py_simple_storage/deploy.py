import json
import os
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_standard, install_solc

from web3.middleware import geth_poa_middleware


load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# Compile Our Solidity
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/967a481528c344a48e7c1a5fcb439df2")
)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
chain_id = 4
my_address = os.environ["MY_ADDRESS"]
private_key = os.environ["PRIVATE_KEY"]
gas_price = w3.eth.gas_price

# Create teh contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the lastest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a transaction
# 2. Sing a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        # "gasPrice": gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sing the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Deployed!")
# Working with the contract, you alway need
# Contract Address
# Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transact -> Actualy make a storage change
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        # "gasPrice": gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("Updated!")
print(simple_storage.functions.retrieve().call())
