import json
import sys
import os
from solcx import compile_standard
from web3 import Web3
from decouple import config

def startCompiling(filePath, filename):

    #       READ FILE
    print("Reading File "+filePath+" .......")
    with open("./"+filePath, "r") as file:
        sol_file = file.read()
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources":{""+filename: {"content":sol_file}},
            "settings":{
                "outputSelection":{
                    "*":{"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            }
        },
        solc_version = "0.6.0",
        )

    #       WRITE FILE
    filenameJSON = filename.split(".")[0]+".json"

    with open("compiled/"+filenameJSON, "w") as file:
        json.dump(compiled_sol, file)

    print("File written to compiled/"+filenameJSON)



    #       GET BYTE CODE
    bytecode = compiled_sol["contracts"][filename][filename.split(".")[0]]["evm"]["bytecode"]["object"]

    #       GET BYTE CODE
    abi = compiled_sol["contracts"][filename][filename.split(".")[0]]["abi"]
    # print(abi)

    #       WRITE ABI TO FILE
    with open("compiled/abi_"+filenameJSON, "w") as file:
        json.dump(abi, file)

    #       CONNECT TO GANACHE
    provider = config('WEB3_PROVIDER')
    w3 = Web3(Web3.HTTPProvider(provider))
    chain_id = int(config('CHAIN_ID'))
    my_address = config('MY_ADDRESS')
    private_key = config('PRIVATE_KEY')


    myContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(my_address)
    # print(chain_id, my_address, private_key, nonce)
    

    # buyer = "0x4E4dc490e276D0F2Ef159bE4eeb933275E358319"
    # seller = "0x29554bA62503d1A8974F95323a7d7c4655f5c450"
    # price = 5

    #       BUILD TRANSACTION
    transaction = myContract.constructor().buildTransaction({"gasPrice":w3.eth.gasPrice, "chainId":chain_id, "from":my_address, "nonce":nonce})
    # print(transaction)
    
    #       SIGN TRANSACTION
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    # print(signed_txn)

    #       SEND TRANSACTION
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_hash)
    print("Contact Address: "+tx_receipt.contractAddress)

###################################################################

#______________________MAIN FUNCTION ______________________________

###################################################################
if(sys.argv[1] == None):
    print("File not specified")
elif(os.path.exists(sys.argv[1])):
    filePath = sys.argv[1]
    filename = os.path.basename(filePath)
    fileDir = os.path.dirname("./"+filePath)
    filesInDir = os.listdir(fileDir)

    # print("Path: "+filePath)
    # print("files in directory: "+fileDir)
    # print(filesInDir)
    # print(filename)

    if filename in filesInDir:
        print("File Found")
        startCompiling(filePath, filename)
    else:
        print("File case doesnt match")
    
else:
    print("File doesnt exists")



