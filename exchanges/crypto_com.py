import os
import time
import hmac
import hashlib
import requests

from constants import MainURLs
from crypto import *
import main_functions

api_key = os.environ['CRYPTO_COM_API_KEY']
private_key = os.environ['CRYPTO_COM_PRIVATE_KEY']

def nonce():
    return str(int(1000*time.time())) 

def get_signature(payload_str: str):
    return hmac.new(
        bytes(str(private_key), 'utf-8'),
        msg=bytes(payload_str, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

def get_balance():
    uri_path = 'private/get-account-summary'
    request = {
        'id': 1200,
        'method': uri_path,
        'api_key': api_key,
        'nonce': nonce(),
        'params': {}
    }
    payload_str = request['method'] + str(request['id']) + request['api_key'] + str(request['nonce'])
    request['sig'] = get_signature(payload_str)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post((MainURLs.CRYPTO_COM_URL.value + '/' + uri_path), json=request, headers=headers)
    
    cryptos = []
    renaming = get_renaming()
    
    for crypto in response.json()['result']['accounts']:
        if (crypto['balance'] > 0):
            cryptos.append( Crypto(
                name=renaming[crypto['currency']],
                short_name=crypto['currency'],
                value=float(crypto['balance']),
                value_in_fiat=main_functions.crypto_to_fiat(renaming[crypto['currency']]) * float(crypto['balance']),
                wallet=Wallet.SPOT
            ))

            
    return cryptos

