from typing import Dict, List, Optional

from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Bus import Bus


class System:
    def __init__(self, name):
        self.name = name
