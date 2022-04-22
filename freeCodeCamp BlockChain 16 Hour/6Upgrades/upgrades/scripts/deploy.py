from brownie import (
    network,
    config,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)
from scripts.helper import encode_fun_data, get_account, upgrade


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(
        {"from": account, "gas": 1000000},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(box.retrieve())
    pa = ProxyAdmin.deploy(
        {"from": account, "gas": 1000000},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    # Basically setting the initialzer function for the contract if not passing initializer then not any issue it will be empty
    # we are able to pass any initial function to here to call if any from our Box contract
    # because we are not using constructor there that's why in this way we are able to call any inital function to set the data
    box_encoded_initializer_fun = encode_fun_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        pa.address,
        box_encoded_initializer_fun,
        {"from": account, "gas": 1000000},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Proxy deployed at {proxy} you can upgrad to v2!")
    # we need to pass abi because it contains function definaltion like interfaces
    # and passes proxy address it will delegate all the functions call to box address
    proxy_box = Contract.from_abi("Box", proxy.address, abi=box.abi)
    # So here you observe we delegate the calls to box address
    proxy_box.store(1, {"from": account, "gas": 1000000})
    print(proxy_box.retrieve())

    # ------------ Now we are going to upgrade to v2 so for that first we deploy v2 version ---------------
    box_v2 = BoxV2.deploy(
        {"from": account, "gas": 1000000},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    upgrade(
        account=account,
        proxy_contract=proxy,
        new_implementation_contract=box_v2,
        proxy_admin_contract=pa,
    )
    print("Proxy has been upgraded!")
    proxy_box_v2 = Contract.from_abi("BoxV2", proxy.address, abi=box_v2.abi)
    proxy_box_v2.increment({"from": account, "gas": 1000000})
    # So we are not to latest version with all the last data like at last there 1 stored but after increment it will be 2 as outcomes show here
    print(proxy_box_v2.retrieve())
