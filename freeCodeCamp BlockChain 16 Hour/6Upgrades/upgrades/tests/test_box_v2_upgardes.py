import pytest
from scripts.helper import encode_fun_data, get_account, upgrade
from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)


def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from": account, "gas": 1000000})
    proxy_admin = ProxyAdmin.deploy({"from": account, "gas": 1000000})
    box_encoded_initializer_fun = encode_fun_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_fun,
        {"from": account, "gas": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, abi=box.abi)

    # deploy boxv2
    box_v2 = BoxV2.deploy({"from": account, "gas": 1000000})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, abi=box_v2.abi)
    # so we not upgrade yet that's why we set it will throw error
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account, "gas": 1000000})
    upgrade(
        account=account,
        proxy_contract=proxy,
        new_implementation_contract=box_v2,
        proxy_admin_contract=proxy_admin,
    )
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account, "gas": 1000000})
    assert proxy_box.retrieve() == 1
