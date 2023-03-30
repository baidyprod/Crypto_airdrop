# Crypto-airdrop by Dmytro Hordiienko

## Disclaimer: the app is working properly and extremely fast if the blockchain is not overloaded. However, when using this software 
in airdrop claims, when thousands of people also try to claim their tokens, the app can work unstable. I have implemented many features
to make this app work stable even in extremal overload conditions.

App needs a folder named "settings" in the same folder as .py files. It contains: main_rpc.txt, side_rpc.txt, token_contract_address.txt, 
token_abi.txt, sender_private_key.txt, recipient_address.txt, threshold.txt

main_rpc.txt - official chain's rpc (connecting be default).

side_rpc.txt - alternative rpc of this chain, could be created by a user. For example using Alchemy website. It is needed if the main rpc
is overloaded.

token_contract_address.txt - the conrtact address of token which needed to be sent. Be careful, the same token in different chain have
different contract addresses.

token_abi.txt - the abi of the token. Can be found on the same page (usually <chain name>scan.com) where you got token contract address.
Scroll down to the contract tab and click copy the abi. Be careful NOT to copy it in json. You need just what is written on the webapge.
  
sender_private_key.txt - sender private key. This private key can be exported from MetaMask.
  
recipient_address.txt - the address of the recipient.
  
threshold.txt - default value is 0. Read the docs on autodetect_and_send.py. If don't have any penny of airdropping token on your wallet 
then use 0 value. If you had some tokens before which are going to be airdropped - run balance_check.py and paste the value in the file.

## autodetect_and_send.py

Continiously checks the balance of the token, and if the balance is higher than the threshold, sends 99,5% token balance to another address
(Your exchange address for example).

## balance_check.py

Checks the balance of token in order to set up threshold.txt right.

## autosender.py

Just sends 99,5% of the token balance to another address (Your exchange address for example).
