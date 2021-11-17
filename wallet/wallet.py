# Import dependencies
import subprocess
import json
import os

# Load and set environment variables
from dotenv import load_dotenv
load_dotenv()
from constants import *
from pprint import pprint

# Import constants.py and necessary functions from bit and web3
# YOUR CODE HERE
# bit
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from bit import wif_to_key
# Web3 
from web3 import Web3, middleware, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware
from eth_account import Account
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# Configure mnemonic via .env
mnemonic = os.getenv('mnemonic')

# Enter private key of the bip39 address
key = wif_to_key("L5UYexkSVa9vroE2usKfzosuzJQdtqefFDcfdZkapdL1SoUKMYxU")

print(key.get_balance('btc'))
print(key.get_balance('usd'))
print(key.get_balance('aud'))

print('----------------')
print(key.get_unspents())

# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols=all --numderive={numderive} --coin={coin} --format=json'
    p = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    (output, err) = p.communicate()
    p_status = p.wait() # this was in our class code but I didn't find a use for it in this file
    return json.loads(output)

    # Create a dictionary object called coins to store the output from `derive_wallets`.
# YOUR CODE HERE
coins = {
    BTC: derive_wallets(mnemonic,BTC,3),
    ETH:derive_wallets(mnemonic,ETH,3),
    BTCTEST: derive_wallets(mnemonic,BTCTEST,3)
}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
    # YOUR CODE HERE
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST: 
        return PrivateKeyTestnet(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
    # YOUR CODE HERE
def create_tx(coin,account,recipient,amount):
    if coin == ETH:
        value = w3.toWei(amount, "ether")
        gasEstimate = w3.eth.estimateGas(
            {"from": account, "to": recipient, "amount": value}
        )
        return {
            "from": address,
            "to": recipient,
            "value": value,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account),
            "chainId": w3.eth.chain_id,
        }
    
    else:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
    # YOUR CODE HERE
def send_tx(coin, account, recipient, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account, recipient, amount)
        signed_tx = account.sign_transaction(raw_tx)
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
#         print(result.hex())
#         return result.hex()
    else:
        raw_tx = create_tx(coin, account, recipient, amount)
        signed_tx = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

pprint(coins)