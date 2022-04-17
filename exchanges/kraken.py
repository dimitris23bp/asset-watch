import urllib.parse
import hashlib
import hmac
import base64
import time
import os
import requests

from constants import MainURLs
import main_functions
from crypto import Crypto

api_key = os.environ['KRAKEN_API_KEY']
private_key = os.environ['KRAKEN_PRIVATE_KEY']
renaming = {
    'ETH': 'ethereum',
    'ETH2': 'ethereum',
    'DOT': 'polkadot',
    'BTC': 'bitcoin',
    'ADA': 'cardano',
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

    staked_cryptos = []
    cryptos = []
    total_cryptos_dict = {}
    for key, value in response.json()['result'].items():
        final_key = key

        if (key not in renaming and key[:-2] not in renaming) or float(value) < 0.01:
            continue
            
        # Add in seperated lists with staked and non-staked
        if key[-2:] == '.S':
            final_key = key[:-2]
            staked_cryptos.append( Crypto(
                name=renaming[final_key], 
                short_name=final_key, 
                value=float(value), 
                value_in_fiat=main_functions.crypto_to_fiat(renaming[final_key]) * float(value)) 
            )
        else:
            cryptos.append( Crypto(
                name=renaming[final_key], 
                short_name=final_key, 
                value=float(value), 
                value_in_fiat=main_functions.crypto_to_fiat(renaming[final_key]) * float(value))
            )

        # Add in dict with total amounts
        if final_key not in total_cryptos_dict:
            total_cryptos_dict[final_key] = Crypto(
                name=renaming[final_key], 
                short_name=final_key, 
                value=float(value), 
                value_in_fiat=main_functions.crypto_to_fiat(renaming[final_key]) * float(value)
            )
        else:
            total_value = total_cryptos_dict[final_key].value  + float(value)
            total_value_in_fiat = main_functions.crypto_to_fiat(renaming[final_key]) * total_value
            total_cryptos_dict[final_key] = Crypto(
                name=renaming[final_key], 
                short_name=final_key, 
                value=total_value,
                value_in_fiat=total_value_in_fiat
            )
            
                
    # TODO: These should be in a seperated file called view_kraken or something similar
    print("Staked:")
    main_functions.display_crypto(staked_cryptos)

    print("Spot:")
    main_functions.display_crypto(cryptos)

    print("Total:")
    main_functions.display_crypto(seperate_from_dict(total_cryptos_dict))

def seperate_from_dict(dictionary: dict):
    list = []

    for key, value in dictionary.items():
        list.append(value)
    
    return list
        