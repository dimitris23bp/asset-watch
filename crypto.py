from dataclasses import dataclass
from enum import Enum

class Wallet(Enum):
    SPOT = "Spot"
    LENDIND = "Lending"
    STAKING = "Staking"

@dataclass
class Crypto:
    name: str
    short_name: str
    value: float
    value_in_fiat: float
    wallet: Wallet = None