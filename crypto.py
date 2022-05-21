from dataclasses import dataclass
from enum import Enum

def get_renaming():
    return {
        'ETH': 'ethereum',
        'ETH2': 'ethereum',
        'DOT': 'polkadot',
        'BTC': 'bitcoin',
        'ADA': 'cardano',
        'SCRT': 'secret',    
        'GODS': 'gods-unchained',
        'UST': 'terrausd',
        'NEXO': 'nexo',
        'PAXG': 'pax-gold',
        'EURX': 'tether-eurt', # CoinGecko doesn't have EURX, so I replace it with another stablecoin
        'DAI': 'dai',
        'USDT': 'tether',
        'CRO': 'crypto-com-chain',
        'USDC': 'usd-coin'
    }

class Wallet(Enum):
    SPOT = "Spot"
    LENDIND = "Lending"
    STAKING = "Staking"

@dataclass
class Crypto:
    name: str
    short_name: str
    value: float
    value_in_fiat: float = None
    wallet: Wallet = None