"""
##################################
#####     Charity Tracker    #####   
#####      Chad Saltzman     #####
#####        12/3/2021       #####
##################################


"""

import json
from web3 import Web3
import sys
from getpass import getpass

def main():

    print("\tCharity Tracker\n")

    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abi = json.loads('[{"inputs":[{"internalType":"string[]","name":"CharityName","type":"string[]"},{"internalType":"address[]","name":"CharityAdd","type":"address[]"}],"stateMutability":"payable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"num","type":"uint256"},{"internalType":"string","name":"trx","type":"string"},{"internalType":"string","name":"CharityName","type":"string"}],"name":"contributeDonation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"UserAddress","type":"address"}],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"searchCharityName","type":"string"}],"name":"getCharityAddress","outputs":[{"internalType":"address","name":"tempAdd","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"trx","type":"string"}],"name":"getStatus","outputs":[{"internalType":"string","name":"status","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"searchCharityName","type":"string"}],"name":"getTotalDonated","outputs":[{"internalType":"uint256","name":"runningTotal","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"newStatus","type":"string"},{"internalType":"string","name":"trx","type":"string"}],"name":"updateStatus","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

    address = web3.toChecksumAddress("0xe0d7A1Ae367010F6Ea2512300f2196c70cB64A69")  # Deployed Contract's address
    contract = web3.eth.contract(address=address, abi=abi)  # Creates an object for the contract.
   
    charityList = {
        "Feeding America": "0x4c2b2972B316d77Ad6C2be9AAa6AbCd845FFB38a",
        "American Red Cross": "0x5D42f081Af27233Ab7ad8fE7039c6B145440d055",
        "St. Jude Children's Research Hospital": "0xDB57c099b403C62388Dfd6a5E5e02fCE83a656E3"
    }
    blockchainOptions = ["Complete a donation", "View the status of a donation", "View the total amount donated", "Update Status", "Verify Charity Address", "Choose a different charity", "Exit"]

    print("Choose a charity from the list below:")
    for i in range(len(charityList)):
        print(str(i+1) + ". " + list(charityList)[i])
    charityValue = int(input())

    
    while True:
        web3.eth.defaultAccount = charityList[list(charityList)[charityValue - 1]]  # Sets the default account to the charities address
        print("Welcome to the " + list(charityList)[charityValue - 1] + " Charity\n")

        print("choose from the following operations:")
        for i in range(len(blockchainOptions)):
            print(str(i+1) + ". " + blockchainOptions[i])
        operationValue = int(input())

        if operationValue == 1:  # Complete a Donation

            donationValue = int(input("Enter in the value of your donation (Ether): "))
            account = input("Enter in your Ethereum Address: ")
            priv_key = getpass("enter in your private key: ")
            nonce = web3.eth.getTransactionCount(account)
            tx = {          #Need to verify the donater has enough ether to donate.
                'nonce': nonce,
                'to': charityList[list(charityList)[charityValue - 1]],
                'value': web3.toWei(donationValue,'ether'),
                'gas': 2000000,
                'data': b"",
                'gasPrice': web3.toWei('50', 'gwei')
            }

            signed_tx = web3.eth.account.signTransaction(tx, priv_key)
            tx_hash = web3.toHex(web3.eth.sendRawTransaction(signed_tx.rawTransaction))
            print(f"You can track the status of this donation with the following hash code: {tx_hash}")
            print(web3.toWei(donationValue,'ether'))
            contract.functions.contributeDonation(web3.toWei(donationValue,'ether'), tx_hash,list(charityList)[charityValue - 1]).transact()

        elif operationValue == 2:  # View the status of a donation
            
            tx = str(input("What is the transaction hash of your donation: "))
            status = contract.functions.getStatus(tx).call()
            print(f"the status of the transaction {tx} is: {status}")

        elif operationValue == 3:  # View the total ammount donated
            balance = contract.functions.getTotalDonated(list(charityList)[charityValue - 1]).call()
            print("\nTotal donated = " + str(web3.fromWei(balance, "ether")) + " ether")

        elif operationValue == 4:  # Update Status
            tx = input("Enter in the hash associated with the donation you would like to update: ")
            status = input("What is the updated status for this transaction: ")
            tx_hash = contract.functions.updateStatus(status,tx).transact()
            print(f"Status has been updated. The transaction hash for this is: {tx_hash}")


        elif operationValue == 5:  # Verify Charity Address
            address = contract.functions.getCharityAddress(list(charityList)[charityValue - 1]).call()
            print(f"The ethereum address of {list(charityList)[charityValue - 1]} is: {address}")

        elif operationValue == 6:  # Switch charities
            print("Choose a charity from the list below:")
            for i in range(len(charityList)):
                print(str(i+1) + ". " + list(charityList)[i])
            charityValue = int(input())

        elif operationValue == 7:  # Exit 
            sys.exit()
    

if __name__ == '__main__':
    main()

