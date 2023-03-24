# Crypto-airdrop

Needad a folder "settings" which contains: main_rpc.txt, side_rpc.txt, token_contract_address.txt, token_abi.txt, 
sender_private_key.txt, recipient_address.txt, threshold.txt

## autodetect_and_send.py

Continiously checks the balance of the token, and if the balance is higher than the threshold, sends 99,5% tokens to another address
(Your exchange address for example).

## balance_check.py

Checks the balance of token in order to set up threshold.txt right.

## autosender.py

Just sends 99,5% tokens from your wallet.
