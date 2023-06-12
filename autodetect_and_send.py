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
        initial_balance = token_contract.functions.balanceOf(sender_address).call()
        print(f'{DEFAULT}Balance: {initial_balance}')

        break

    except Exception as e:
        print(f'{WARNING}Unable to get initial balance, probably the RPC is overloaded')
        print(f'{WARNING}{e}')
        print(f'{DEFAULT}Getting initial balance one more time')


if initial_balance <= int(threshold):
    print(f'{DEFAULT}Balance is less than {int(threshold)}. Waiting for tokens')
    while True:
        while True:
            try:
                current_balance = token_contract.functions.balanceOf(sender_address).call()
                break

            except Exception as e:
                print(f'{WARNING}Unable to get current balance, probably the RPC is overloaded')
                print(f'{WARNING}{e}')
                print(f'{DEFAULT}Getting current balance one more time')

        if current_balance != initial_balance:
            print(f'{SUCCESS}Balance change detected!')
            print(f'{DEFAULT}Current balance: {current_balance}')

            break

        time.sleep(round(random.uniform(0.25, 0.8), 3))

else:
    current_balance = initial_balance


try:
    print(f'{DEFAULT}Setting a transaction with automatic gas value')
    tx = token_contract.functions.transfer(recipient_address, int(current_balance * 0.995)).build_transaction({
        'gas': 30000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(sender_address),
        'chainId': w3.eth.chain_id
    })

    gas_estimate = token_contract.functions.transfer(recipient_address, int(current_balance * 0.995)).estimate_gas({
        'from': sender_address
    })
    tx['gas'] = gas_estimate
    print(f'{SUCCESS}Transaction set!')

    print(f'{DEFAULT}Sending tokens with {tx["gas"]} gas')
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=sender_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f'{SUCCESS}Successfully sent {current_balance * 0.995} tokens to {recipient_address}')

except Exception as e:
    print(f'{WARNING}{e}')
    print(f'{DEFAULT}Trying again with manual gas setting!')

    gas = 100000
    multiplier = 5

    while True:
        try:
            print(f'{DEFAULT}Setting a transaction')
            tx = token_contract.functions.transfer(recipient_address, int(current_balance * 0.995)).build_transaction({
                'gas': int(gas * multiplier),
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(sender_address),
                'chainId': w3.eth.chain_id
            })

            print(f'{DEFAULT}Sending tokens with {tx["gas"]} gas')
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=sender_private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'{SUCCESS}Successfully sent {current_balance * 0.995} tokens to {recipient_address}')

            break

        except Exception as e:
            print(f'{WARNING}{e}')
            multiplier += 5
            print(f'{DEFAULT}Trying again with {gas * multiplier}')

        time.sleep(round(random.uniform(0.1, 0.3), 3))
