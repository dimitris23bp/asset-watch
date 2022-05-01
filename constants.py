from enum import Enum

class Exchanges(Enum):
    KRAKEN = "Kraken"
    FTX = "FTX"
    NEXO = "Nexo"

class CryptoNames(Enum):
    BTC = "BTC:  Bitcoin"
    ETH = "ETH:  Ether"
    DOT = "DOT:  Polkadot"
    ADA = "ADA:  Cardano"
    GODS = "GODS: Gods Unchained"

class MainURLs(Enum):
    COIN_GECKO = "https://api.coingecko.com/api/v3"
    KRAKEN_URL = "https://api.kraken.com"
    FTX_URL = "https://ftx.com"

class CoinGecko(Enum):
    CRYPTO_TO_FIAT = "/coins/{0}" # Add full name of crypto (eg Ethereum)