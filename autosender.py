from web3 import Web3, types
import time
import random

SUCCESS = '\033[92m'
WARNING = '\033[93m'
DEFAULT = '\033[0m'


def read_files(*files):
    results = []
    for file_name in files:
        with open(file_name, 'r') as f:
            results.append(f.read())
    return results


main_rpc, side_rpc, token_contract_address, abi, sender_private_key, recipient_address_unconverted = read_files(
                                                                                 'settings/main_rpc.txt',
                                                                                 'settings/side_rpc.txt',
                                                                                 'settings/token_contract_address.txt',
                                                                                 'settings/token_abi.txt',
                                                                                 'settings/sender_private_key.txt',
                                                                                 'settings/recipient_address.txt')


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
