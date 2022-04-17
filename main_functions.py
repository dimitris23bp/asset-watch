import requests
import logging
from prettytable import PrettyTable

from constants import Exchanges, CoinGecko, MainURLs
import exchanges.kraken as kraken
import exchanges.ftx as ftx
from crypto import * 

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
    return float(response.json()['market_data']['current_price']['eur'])

    
def display_all_wallets(cryptos: list[Crypto]):
    staked_cryptos = {} 
    lended_cryptos = {}
    spot_cryptos = {}
    total_cryptos = {}
    for crypto in cryptos:
        if crypto.wallet == Wallet.STAKING:
            if crypto.short_name in staked_cryptos:
                value_before = staked_cryptos[crypto.short_name].value
                staked_cryptos[crypto.short_name] = Crypto(
                    short_name=crypto.short_name,
                    name=crypto.name,
                    value=(crypto.value + value_before),
                    value_in_fiat=( crypto_to_fiat(crypto.name) * (crypto.value + value_before) ),
                    wallet=Wallet.STAKING
                )
            else:
                staked_cryptos[crypto.short_name] = crypto
        elif crypto.wallet == Wallet.LENDIND:
            if crypto.short_name in lended_cryptos:
                value_before = lended_cryptos[crypto.short_name].value
                lended_cryptos[crypto.short_name] = Crypto(
                    short_name=crypto.short_name,
                    name=crypto.name,
                    value=(crypto.value + value_before),
                    value_in_fiat=( crypto_to_fiat(crypto.name) * (crypto.value + value_before) ),
                    wallet=Wallet.LENDIND
                )
            else:
                lended_cryptos[crypto.short_name] = crypto
        elif crypto.wallet == Wallet.SPOT:
            if crypto.short_name in spot_cryptos:
                value_before = spot_cryptos[crypto.short_name].value
                spot_cryptos[crypto.short_name] = Crypto(
                    short_name=crypto.short_name,
                    name=crypto.name,
                    value=(crypto.value + value_before),
                    value_in_fiat=( crypto_to_fiat(crypto.name) * (crypto.value + value_before) ),
                    wallet=Wallet.LENDIND
                )
            else:
                spot_cryptos[crypto.short_name] = crypto
        
        if crypto.short_name in total_cryptos:
            value_before = total_cryptos[crypto.short_name].value
            total_cryptos[crypto.short_name] = Crypto(
                short_name=crypto.short_name,
                name=crypto.name,
                value=(crypto.value + value_before),
                value_in_fiat=( crypto_to_fiat(crypto.name) * (crypto.value + value_before) )
            )
        else:
            total_cryptos[crypto.short_name] = crypto
    
       
    if len(staked_cryptos) > 0:
        print("Staked:")
        display_crypto(seperate_from_dict(staked_cryptos))

    if len(lended_cryptos) > 0:
        print("Lended:")
        display_crypto(seperate_from_dict(lended_cryptos))

    if len(spot_cryptos) > 0:
        print("Spot:")
        display_crypto(seperate_from_dict(spot_cryptos))

    if len(total_cryptos) > 0:
        print("Total:")
        display_crypto(seperate_from_dict(total_cryptos))
            
            
            
    
def display_crypto(data: list):
    x = PrettyTable()
    for crypto in data:
        x.field_names = ["Crypto", "Amount", "Value"]
        x.add_row([crypto.short_name, round(crypto.value, 8), round(crypto.value_in_fiat, 2)])

    print(x)
    print()

def show_total():
    for exchange in get_specific_accounts()[:-1]:
        show_account(exchange)
        # Get data from an exchange
        
        
        # Get data to the total amount

def seperate_from_dict(dictionary: dict):
    list = []

    for key, value in dictionary.items():
        list.append(value)
    
    return list