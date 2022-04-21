from brownie import SimpleStorage, accounts


# Every time new Test starts from inital stage
def test_deploy():
    # Test Having Three Stages => Arrange, Act, Assert

    # Arrange
    account = accounts[0]
    # Act
    ss = SimpleStorage.deploy({"from": account})
    # Assert // Initial retrieve value is 0
    assert ss.retrieve() == 0


def test_updating_storage():
    # Arrange
    account = accounts[0]
    ss = SimpleStorage.deploy({"from": account})

    # Act
    transaction = ss.store(10, {"from": account})
    transaction.wait(1)

    # Assert
    assert ss.retrieve() == 10
