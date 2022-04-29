import pytest

import pytest
from web3 import Web3


# It is just like static const but for test we use this


@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")
