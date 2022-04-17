import urllib.parse
import hashlib
import hmac
import base64
import time
import os
import requests

from constants import MainURLs
import main_functions
from crypto import *

api_key = os.environ['KRAKEN_API_KEY']
private_key = os.environ['KRAKEN_PRIVATE_KEY']
renaming = {
    'ETH': 'ethereum',
    'ETH2': 'ethereum',
    'DOT': 'polkadot',
    'BTC': 'bitcoin',
    'ADA': 'cardano',
    'SCRT': 'secret',
}

def nonce():
    return str(int(1000*time.time())) 

def get_signature(urlpath, data):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(private_key), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def get_headers(uri_path, data):
    return {'API-Key': api_key, 'API-Sign': get_signature(uri_path, data)}


def get_balance(data):
    uri_path = '/0/private/Balance'
    response = requests.post((MainURLs.KRAKEN_URL.value + uri_path), headers=get_headers(uri_path, data), data=data)

    cryptos = []
    for key, value in response.json()['result'].items():
        final_key = key

        if (key not in renaming and key[:-2] not in renaming) or float(value) < 0.01:
            continue
            
        # Add in seperated lists with staked and non-staked
        if key[-2:] == '.S':
            final_key = key[:-2]
            cryptos.append( Crypto(
                name=renaming[final_key], 
                short_name=final_key, 
                value=float(value), 
                value_in_fiat=main_functions.crypto_to_fiat(renaming[final_key]) * float(value),
                wallet=Wallet.STAKING
            ))
        else:
            cryptos.append( Crypto(
                name=renaming[final_key], 
                short_name=final_key, 
                value=float(value), 
                value_in_fiat=main_functions.crypto_to_fiat(renaming[final_key]) * float(value),
                wallet=Wallet.SPOT
            ))
    return cryptos