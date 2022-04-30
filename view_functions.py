from xmlrpc.client import Boolean
from main_functions import *
from prettytable import PrettyTable

def display_all():
    staked_cryptos = {}
    lended_cryptos = {}
    spot_cryptos = {}
    total_cryptos = {}
    get_total(staked_cryptos, lended_cryptos, spot_cryptos, total_cryptos)

    if len(staked_cryptos) > 0:
        print("Staked:")
        display_wallet(seperate_from_dict(staked_cryptos))

    if len(lended_cryptos) > 0:
        print("Lended:")
        display_wallet(seperate_from_dict(lended_cryptos))

    if len(spot_cryptos) > 0:
        print("Spot:")
        display_wallet(seperate_from_dict(spot_cryptos))

    if len(total_cryptos) > 0:
        print("Total:")
        display_wallet(seperate_from_dict(total_cryptos))

def display_wallet(data: list):
    x = PrettyTable()
    for crypto in data:
        x.field_names = ["Crypto", "Amount", "Value"]
        x.add_row([crypto.short_name, round(crypto.value, 8), round(crypto.value_in_fiat, 2)])
    print(x)
    print()

def display_exchange(cryptos: list[Crypto]):
    staked_cryptos = {}
    lended_cryptos = {}
    spot_cryptos = {}
    total_cryptos = {}
    get_all_wallets(staked_cryptos, lended_cryptos, spot_cryptos, total_cryptos, cryptos)
    
    if len(staked_cryptos) > 0:
        print("Staked:")
        display_wallet(seperate_from_dict(staked_cryptos))

    if len(lended_cryptos) > 0:
        print("Lended:")
        display_wallet(seperate_from_dict(lended_cryptos))

    if len(spot_cryptos) > 0:
        print("Spot:")
        display_wallet(seperate_from_dict(spot_cryptos))

    if len(total_cryptos) > 0:
        print("Total:")
        display_wallet(seperate_from_dict(total_cryptos))

def display_asset(asset_name: str):
    staked_cryptos = {}
    lended_cryptos = {}
    spot_cryptos = {}
    total_cryptos = {}
    final_values = []
    name = [crypto_name.name for crypto_name in CryptoNames if asset_name == crypto_name.value][0]
    get_total(staked_cryptos, lended_cryptos, spot_cryptos, total_cryptos)

    table = PrettyTable()
    table.field_names = ["Crypto", "Spot", "Staked", "Lended", "Total", "Value"]
    final_values.append(name)

    # Add a value for each one of the categories
    add_value_from_asset(spot_cryptos, final_values, name)
    add_value_from_asset(staked_cryptos, final_values, name)
    add_value_from_asset(lended_cryptos, final_values, name)
    add_value_from_asset(total_cryptos, final_values, name, True)

    table.add_row(final_values)
    print(table)

# Get value from asset in the specific wallet
def add_value_from_asset(wallet: dict[Crypto], final_values: list, name: str, total: Boolean = False):
    exists = False
    for _, value in wallet.items():
        if value.short_name == name:
            final_values.append(value.value)
            if total:
                final_values.append(round(value.value_in_fiat, 2))
            exists = True
    if exists == False: final_values.append(0)
    # TODO: This should be removed when I display only the assets that actually exists, thus, get them from a DB instead of a hashmap
    # Add an extra zero in case there is no asset with that name
    if len(final_values) != 6 and total: final_values.append(0)