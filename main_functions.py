import requests
from constants import Exchanges, CoinGecko, MainURLs
import logging
import exchanges.kraken as kraken
import exchanges.ftx as ftx
from prettytable import PrettyTable

def get_specific_accounts():
    return [Exchanges.KRAKEN.value, Exchanges.FTX.value, "Back"]

def show_account(account_name):
    match account_name:
        case Exchanges.KRAKEN.value:
            logging.info("In Kraken acount")
            return kraken.get_balance({"nonce": kraken.nonce()})
        case Exchanges.FTX.value:
            logging.info("In FTX account")
            return ftx.get_balance()

def crypto_to_fiat(crypto_name, fiat_name='eur'):
    params = {'localization': 'false', 'tickers': 'false', 'community_data': 'false', 'developer_data': 'false'}
    name = MainURLs.COIN_GECKO.value + CoinGecko.CRYPTO_TO_FIAT.value.format(crypto_name)
    response = requests.get(name, params=params)
    print(crypto_name)
    return float(response.json()['market_data']['current_price']['eur'])

    
def display_crypto(data: dict):
    x = PrettyTable()
    at_least_one = False
    for crypto in data:
        x.field_names = ["Crypto", "Amount", "Value"]
        x.add_row([crypto.short_name, crypto.value, crypto.value_in_fiat])
        at_least_one = True

    if at_least_one:
        print(x)
    else:
        print("Empty")
    print()