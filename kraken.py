import urllib.parse
import hashlib
import hmac
import base64
import time
import requests
import os

api_url = "https://api.kraken.com"
api_key = os.environ['KRAKEN_API_KEY']
private_key = os.environ['KRAKEN_PRIVATE_KEY']
nonce = str(int(1000*time.time()))

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req


response = kraken_request('/0/private/Balance', {"nonce": nonce}, api_key, private_key)

print(response.json())        