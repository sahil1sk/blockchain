// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

// [^0.6.0 (this will work with any version below 0.7 and above 0.6 this is another example)]
// [Every time define version first]

contract SimpleStorage {
    // this will get initialize to zero
    uint256 public favoriteNumeber;

    struct People {
        uint256 favoriteNumeber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    // memory or storage (memory during the execution only (after execution delete this forever) )
    // (storage persist the data (after execution persist it))
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumeber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    People public person = People({favoriteNumeber: 2, name: "Sahil"});

    function store(uint256 _favoriteNumber) public {
        favoriteNumeber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumeber;
    }

    function sum(uint256 _favoriteNumeber) public pure returns (uint256) {
        // favoriteNumeber + favoriteNumeber;
        _favoriteNumeber += _favoriteNumeber;
        return _favoriteNumeber;
    }
}
