from enum import Enum

class Exchanges(Enum):
    KRAKEN = "Kraken"
    FTX = "FTX"

class MainURLs(Enum):
    COIN_GECKO = "https://api.coingecko.com/api/v3"
    KRAKEN_URL = "https://api.kraken.com"

class CoinGecko(Enum):
    CRYPTO_TO_FIAT = "/coins/{0}" # Add full name of crypto (eg Ethereum)