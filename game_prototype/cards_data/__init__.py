# This file makes the 'cards_data' directory a Python package.
# It's used to aggregate all the individual card definitions.

from .qian import QIAN_WEI_TIAN

# As new card files (e.g., kun.py) are added, they will be imported here.

ALL_CARDS = [
    QIAN_WEI_TIAN,
    # Future cards will be added to this list.
]
