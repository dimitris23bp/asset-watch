import hmac
import requests
import os
import time
from constants import MainURLs
from crypto import Crypto, Wallet
import main_functions

api_key = os.environ['FTX_API_KEY']
private_key = os.environ['FTX_PRIVATE_KEY']
renaming = {
    'GODS': 'gods-unchained'
}
def get_nonce():
    return str(int(1000*time.time())) 

def get_signature(method, url_path, nonce):
    signature_payload = f'{int(nonce)}{method}{url_path}'.encode()
    return hmac.new(private_key.encode(), signature_payload, 'sha256').hexdigest()

def get_headers(method, url_path):
    nonce = get_nonce()
    return {
        'FTX-KEY': api_key, 
        'FTX-SIGN': get_signature(method, url_path, nonce),
        'FTX-TS': nonce
    }


def get_balance():
    path_url = '/api/wallet/balances'
    response = requests.get(MainURLs.FTX_URL.value + path_url, headers=get_headers('GET', path_url))

    cryptos = []
    for crypto in response.json()['result']:
        if crypto['total'] == 0.0 or crypto['coin'] not in renaming:
            continue

        cryptos.append( Crypto(
            name=renaming[crypto['coin']],
            short_name=crypto['coin'],
            value=float(crypto['total']),
            value_in_fiat=main_functions.crypto_to_fiat(renaming[crypto['coin']]) * float(crypto['total']),
            wallet=Wallet.SPOT
        ))
        
    return cryptos

        