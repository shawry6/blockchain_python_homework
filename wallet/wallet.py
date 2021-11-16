# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os


# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
# YOUR CODE HERE
from constants import *
from bit import wif_to_key
from bit import Key, PrivateKey, PrivateKeyTestnet
from bit.network import NetworkAPI
from eth_account import Account
from web3 import Web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Enter private key of the bip39 address
key = wif_to_key("L5UYexkSVa9vroE2usKfzosuzJQdtqefFDcfdZkapdL1SoUKMYxU")

print(key.get_balance('btc'))
print(key.get_balance('usd'))
print(key.get_balance('aud'))

print('----------------')
print(key.get_unspents())
 
 
# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = 'php derive -g --mnemonic --cols=path,address,privkey,pubkey --coin --numderive --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output 
# from `derive_wallets`.
# YOUR CODE HERE
# coins = {['btc'], ['eth'], ['btc-test']}
coins = {'btc': derive_wallets(mnemonic=mnemonic,coin=BTC,numderive=3),'eth':derive_wallets(mnemonic=mnemonic,coin=ETH,numderive=3),'btc-test': derive_wallets(mnemonic=mnemonic,coin=BTCTEST,numderive=3)}
# print(json.dumps(coins, indent=4, sort_keys=True))

btc_key = coins['btc'][0]['privkey']
eth_key = coins['eth'][0]['privkey']
btctest_key = coins['btc-test'][0]['privkey']
# print(btc_key)
# print(eth_key)
# print(btctest_key)

btc_recipient = coins['btc'][1]['address']
eth_recipient = coins['eth'][1]['address']
btctest_recipient = coins['btc-test'][1]['address']
# print(btc_recipient)
# print(eth_recipient)
# print(btctest_recipient)

# Create a function called `priv_key_to_account` that converts 
# privkey strings to account objects.
    # YOUR CODE HERE
def priv_key_to_account(coin, priv_key):
    global account
    if coin == 'eth':
        account=Account.privateKeyToAccount(priv_key)
    else:
        account=PrivateKeyTestnet(priv_key)
    return account


# Create a function called `create_tx` that creates an unsigned 
# transaction appropriate metadata.
    # YOUR CODE HERE
def create_tx(coin,account,recipient,amount):
    global tx_data
    if coin =='eth':
        gasEstimate = w3.eth.estimateGas(
#             {"from": account.address, "to": recipient, "value": amount}
            {"from": eth_add, "to": eth_recipient, "value": amount}
        )
        tx_data= {
#             "from": account.address,
            "from": eth_add,
            "to": eth_recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_add),
        }
        return tx_data
    else:
        tx_data = PrivateKeyTestnet.prepare_transaction(account.address, [(btctest_recipient, amount, BTC)])
        return tx_data

# Create a function called `send_tx` that calls `create_tx`, 
# signs and sends the transaction.
    # YOUR CODE HERE
def send_tx(coin, account, recipient, amount):
    if coin == ETH:
        tx = create_tx(coin,account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    else:
        tx_data = create_tx(coin,account,recipient,amount)
        signed = account.sign_transaction(tx_data)
        NetworkAPI.broadcast_tx_testnet(signed)
        return signed
