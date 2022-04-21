import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv

# pip install py-solc-x
# pip install web3
# pip install python-dotenv (for env variables loading from .env file if any .env file exists)

# load .env file if any
load_dotenv()

# Install Solc version which we used
install_solc(os.getenv("SOLC_VERSION"))

# Reading the solidity file
with open("./SimpleStorage.sol", "r") as f:
    simple_storage_file = f.read()

# Compile the solidity code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {"outputSelection": {"*": {"*": ["*"]}}},
    },
    solc_version=os.getenv("SOLC_VERSION"),
)

# Write the compiled output to a JSON file
with open("compiled_code.json", "w") as f:
    json.dump(compiled_sol, f)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# ------- REMEMBER NEVER HARD CODE YOUR SENSITIVE INFORMATION ----------

# For connection to ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("GANACHE_URL")))

# we are getting the properties from env file .env which we loaded using  load_dotenv function
# if file not present it will try to get properties from OS ENV Directly

chain_id = os.getenv("CHAIN_ID")
my_address = os.getenv("ACC_ADDRESS")
private_key = os.getenv("ACC_PRIVATE_KEY")

# Create the contract in python (This means we create the contract not deployed the contract)
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)


# Get the latest transction count
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

## IN case to deploy
# 1 BUild the contract deploy transaction,
# 2 Sign the Transaction,
# 3 Send the transaction

# As we know all contracts have implict constructor if we not declared explicitly as in the class in java
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "from": my_address,
        "nonce": nonce,
        # "chainId": chain_id,
        "chainId": w3.eth.chainId,
        "gas": 1000000,
        "gasPrice": w3.toWei("10", "gwei"),
    }
)

# print(transaction)

# Sign the transaction with our private key so that others can verify it by our public address
signed_transaction = w3.eth.account.signTransaction(transaction, private_key)
# print(signed_transaction)

# Send this signed transaction to the network
transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
# wait till the completion of the transaction
transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)

# Working with the contract, you always need
# Contract Address
# Contract ABI (Application Binary Interface)
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

print("Contract Address: ", transaction_receipt.contractAddress, "\nContract Deployed")

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# calling retrive function initially value is 0
print(simple_storage.functions.retrieve().call())
print("Updating Contract")

# Setting the value to 50 (So it is state change make new transaction)
store_transaction = simple_storage.functions.store(50).buildTransaction(
    {
        "from": my_address,
        "nonce": w3.eth.getTransactionCount(my_address),  # get the latest nonce
        # "chainId": chain_id,
        "chainId": w3.eth.chainId,
        "gas": 1000000,
        "gasPrice": w3.toWei("10", "gwei"),
    }
)

signed_store_transaction = w3.eth.account.signTransaction(
    store_transaction, private_key
)

store_transaction_hash = w3.eth.sendRawTransaction(
    signed_store_transaction.rawTransaction
)
store_transaction_receipt = w3.eth.waitForTransactionReceipt(store_transaction_hash)


# Transact (Easy way to do it) if you don't need any hash or receipt back to do on operation further
# simple_storage.functions.store(5).transact({"from": my_address, "gas": 1000000})


# to get the stored value
print(simple_storage.functions.retrieve().call())
