# This file makes the 'cards_data' directory a Python package.
# It's used to aggregate all the individual card definitions.

from .qian import QIAN_WEI_TIAN
from .kun import KUN_WEI_DI

# As new card files are added, they will be imported here.

ALL_CARDS = [
    QIAN_WEI_TIAN,
    KUN_WEI_DI,
    # Future cards will be added to this list.
]
