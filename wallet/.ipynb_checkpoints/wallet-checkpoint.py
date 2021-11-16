# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
from constants import *

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
# YOUR CODE HERE
from constants import *
from bit import wif_to_key

# Enter private key of the bip39 address
key = wif_to_key("cS7Uou68ZHEN5iYrG77o5WbWWwwsTBWjFm8dH3JBjSXKQzP4fsUY")

print(key.get_balance('btc'))
print(key.get_balance('usd'))
print(key.get_balance('aud'))

print('----------------')
print(key.get_unspents())
 
 
# Create a function called `derive_wallets`
def derive_wallets(# YOUR CODE HERE):
    command = 'php derive -g --mnemonic --cols=path,address,privkey,pubkey #--format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output 
# from `derive_wallets`.
# YOUR CODE HERE
coins = {['btc'], ['eth'], ['btc-test']}

# Create a function called `priv_key_to_account` that converts 
# privkey strings to account objects.
def priv_key_to_account(# YOUR CODE HERE):
    # YOUR CODE HERE

# Create a function called `create_tx` that creates an unsigned 
# transaction appropriate metadata.
def create_tx(# YOUR CODE HERE):
    # YOUR CODE HERE

# Create a function called `send_tx` that calls `create_tx`, 
# signs and sends the transaction.
def send_tx(# YOUR CODE HERE):
    # YOUR CODE HERE

