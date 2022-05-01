import requests
import logging

from constants import *
import exchanges.kraken as kraken
import exchanges.ftx as ftx
import exchanges.nexo as nexo
from crypto import * 

# TODO: Add database and get the current accounts, instead of adding them manually
def get_specific_exchange():
    return [Exchanges.KRAKEN.value, Exchanges.FTX.value, Exchanges.NEXO.value, "Back"]

def get_specific_asset():
    crypto_names = []
    for crypto_name in CryptoNames:
        crypto_names.append(crypto_name.value)
    crypto_names.append("Back")
    return crypto_names

def get_balance_from_exchange(account_name):
    match account_name:
        case Exchanges.KRAKEN.value:
            logging.info("In Kraken acount")
            return kraken.get_balance({"nonce": kraken.nonce()})
        case Exchanges.FTX.value:
            logging.info("In FTX account")
            return ftx.get_balance()
        case Exchanges.NEXO.value:
            logging.info("In Nexo account")
            return nexo.get_balance()
            

def crypto_to_fiat(crypto_name, fiat_name='eur'):
    params = {'localization': 'false', 'tickers': 'false', 'community_data': 'false', 'developer_data': 'false'}
    name = MainURLs.COIN_GECKO.value + CoinGecko.CRYPTO_TO_FIAT.value.format(crypto_name)
    response = requests.get(name, params=params)
    return float(response.json()['market_data']['current_price']['eur'])
    
def get_all_wallets(staked_cryptos: dict, lended_cryptos: dict, spot_cryptos: dict, total_cryptos: dict, cryptos: list[Crypto]):
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
            
def get_total(staked_cryptos: dict, lended_cryptos: dict, spot_cryptos: dict, total_cryptos: dict):
    for exchange in get_specific_exchange()[:-1]:
        # Get data from an exchange
        current_account_balance = get_balance_from_exchange(exchange)
        # Get data to the total amount
        get_all_wallets(staked_cryptos, lended_cryptos, spot_cryptos, total_cryptos, current_account_balance)

def seperate_from_dict(dictionary: dict):
    list = []
    for _, value in dictionary.items():
        list.append(value)
    return list

def get_name_from_value(value: str):
    # for crypto_name in CryptoNames:
    #     if value is crypto_name.value:
    #         return crypto_name.name
        
    # return crypto_name.name if value is crypto_name.value in CryptoNames else None
    return ([crypto_name.name for crypto_name in CryptoNames if value is crypto_name.value])