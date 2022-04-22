from scripts.helper import encode_fun_data, get_account
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegates_calls():
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

    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account, "gas": 1000000})
    assert proxy_box.retrieve() == 1
