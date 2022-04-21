// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "./1SimpleStorage.sol";

// is SimpleStorage (inheritance)
contract StorageFactory is SimpleStorage {
    SimpleStorage[] public simpleStorageArray;
    
    function createSimpleStorageContract() public {
        // so here we creating the new contract from this StorageFactory Contract deploying contract from the contract
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        // Any time we interact with contract we need to things Address and ABI
        // Address of the contract to interact with
        // ABI = (Application Binary Input) 
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        // store is the function which we made in SimpleStorage contract
        simpleStorage.store(_simpleStorageNumber);
    }

    function sfGet(uint256 _simpleStorageIndex) public view returns(uint256) {
        return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve();
    } 
}

