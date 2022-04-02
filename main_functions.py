from constants import Constants
import logging
import kraken
from constants import Constants

def get_specific_accounts():
    return [Constants.KRAKEN.value, "Other stuff", "Back"]

def show_account(account_name):
    match account_name:
        case Constants.KRAKEN.value:
            logging.info("In Kraken acount")
            return kraken.kraken_request('/0/private/Balance', {"nonce": kraken.nonce()})
        case Constants.FTX.value:
            logging.info("In FTX account")