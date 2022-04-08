from dataclasses import dataclass


@dataclass
class Crypto:
    name: str
    short_name: str
    value: float
    value_in_fiat: float