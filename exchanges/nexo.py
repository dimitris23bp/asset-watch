import csv
from crypto import *
import main_functions
import logging

def get_balance():
    cryptos = {}
    with open('nexo_transactions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        renaming = get_renaming()
        for row in reversed(list(csv_reader)[1:]):
            transaction_type = row[1]
            short_name = row[4]
            if short_name not in renaming:
                logging.error(f"{short_name} doesn't exist in renaming. That crypto will be skipped.")
                continue

            if transaction_type in ("Interest", "Exchange Cashback", "FixedTermInterest", "DepositToExchange", "Exchange"):
                if short_name in cryptos:
                    temp_crypto = cryptos[short_name]
                    cryptos[short_name] = Crypto(
                        name=renaming[short_name],
                        short_name=short_name,
                        value=temp_crypto.value + float(row[5]),
                        wallet=Wallet.LENDIND
                    )
                else:
                    cryptos[short_name] = Crypto(
                        name=renaming[short_name],
                        short_name=short_name,
                        value=float(row[5]),
                        wallet=Wallet.LENDIND
                   )
            # Extra steps if it is a transaction crypto-to-crypto
            if transaction_type in ('Exchange'):
                temp_crypto = cryptos[row[2]]
                cryptos[temp_crypto.short_name] = Crypto(
                    short_name=temp_crypto.short_name,
                    name=temp_crypto.name,
                    value=temp_crypto.value - abs(float(row[3])),
                    wallet=Wallet.LENDIND
                )
                
    cryptos = main_functions.seperate_from_dict(cryptos)    
    for crypto in reversed(cryptos):
        crypto.value_in_fiat = main_functions.crypto_to_fiat(renaming[crypto.short_name]) * crypto.value
        if crypto.value_in_fiat < 0.01: cryptos.remove(crypto)
    return cryptos