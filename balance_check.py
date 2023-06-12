import os
import time
import random

from dotenv import load_dotenv

from web3 import Web3, types


load_dotenv()

SUCCESS = '\033[92m'
WARNING = '\033[93m'
DEFAULT = '\033[0m'


main_rpc = os.getenv('MAIN_RPC')
side_rpc = os.getenv('SIDE_RPC')
token_contract_address = os.getenv('TOKEN_CONTRACT_ADDRESS')
abi = os.getenv('ABI')
sender_private_key = os.getenv('SENDER_PRIVATE_KEY')
recipient_address_unconverted = os.getenv('RECIPIENT_ADDRESS')
threshold = os.getenv('THRESHOLD')


while True:
    try:
        print(f'{DEFAULT}Connecting to main network')
        w3 = Web3(Web3.HTTPProvider(main_rpc))
        print(f'{SUCCESS}Successfully connected to main network!')

        break

    except Exception as e:
        print(f'{WARNING}{e}')
        print(f'{DEFAULT}Connecting to side network')

        try:
            w3 = Web3(Web3.HTTPProvider(side_rpc))
            print(f'{SUCCESS}Successfully connected to side network!')

            break

        except Exception as e:
            print(f'{WARNING}{e}')
            print(f'{DEFAULT}Once again')


recipient_address = w3.to_checksum_address(recipient_address_unconverted)

token_contract = w3.eth.contract(address=w3.to_checksum_address(types.Address(token_contract_address)), abi=abi)

sender_address = w3.eth.account.from_key(sender_private_key).address


while True:
    try:
        current_balance = token_contract.functions.balanceOf(sender_address).call()
        print(f'{DEFAULT}Balance: {current_balance}')

        break

    except Exception as e:
        print(f'{WARNING}Unable to get current balance, probably the RPC is overloaded')
        print(f'{WARNING}{e}')
        print(f'{DEFAULT}Getting current balance one more time')
