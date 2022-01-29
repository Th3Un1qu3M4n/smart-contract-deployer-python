import json
import sys
import os
from solcx import compile_standard
from web3 import Web3
from decouple import config


def setContract(buyer, seller, price):
        setup_txn = Escrow_contract.functions.setupContract(buyer,seller,price).buildTransaction({"gasPrice":w3.eth.gasPrice, "chainId":chain_id, "from":my_address, "nonce":nonce})
        signed_setup_txn = w3.eth.account.sign_transaction(setup_txn, private_key=private_key)

        tx_hash = w3.eth.send_raw_transaction(signed_setup_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Transaction Hash: \n"+str(tx_receipt.transactionHash))


with open("compiled/abi_escrow.json", "r") as file:
        abi = json.load(file)

provider = config('WEB3_PROVIDER')
w3 = Web3(Web3.HTTPProvider(provider))
chain_id = int(config('CHAIN_ID'))
my_address = config('MY_ADDRESS')
private_key = config('PRIVATE_KEY')
nonce = w3.eth.getTransactionCount(my_address)

Escrow_contract = w3.eth.contract(address=sys.argv[1], abi=abi)
currState = Escrow_contract.functions.currState().call()
print("\nOwner: "+Escrow_contract.functions.owner().call())
print("State: "+str(currState))
print("Buyer: "+str(Escrow_contract.functions.buyer().call()))
print("Seller: "+str(Escrow_contract.functions.seller().call()))

if(currState==0):
        doSetup = input("\nDo you want to setup Contract?(Y/N)")
        if(doSetup=='Y'):
                print("setting up contract")
                setContract("0x29554bA62503d1A8974F95323a7d7c4655f5c450","0xC7753b920E48c252225ef766a63Fcdd47EB3DDD2",5)
else:
        print("\nContract Already Setup")


