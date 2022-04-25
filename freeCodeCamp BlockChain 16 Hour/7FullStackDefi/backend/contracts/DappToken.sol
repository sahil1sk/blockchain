// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DappToken is ERC20 {
    // Name and Symbol => OurToken, OT
    constructor(uint256 initialSupply) ERC20("Dapp Token", "DAPP") {
        _mint(msg.sender, initialSupply);
    }
}
