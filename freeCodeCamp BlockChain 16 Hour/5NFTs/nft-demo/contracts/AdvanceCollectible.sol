// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract AdvanceCollectible is ERC721 {
    uint256 public tokenCounter;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public tokenIdToBreed;
    // It is a good practice whenever we update the mapping then trigger a event
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    // mapping(bytes32 => address) public requestIdToSender;

    // First add the Name of the token and then add the symbol
    constructor() public ERC721("Dogie", "DOG") {
        tokenCounter = 0;
    }

    function createCollectible() public returns (uint256) {
        // We are able to use VRFConsumer to generate Random Number but we are using this approach for now
        uint256 rn = uint256(
            keccak256(
                abi.encodePacked(
                    // nonce, // nonce is preditable (aka, transaction number)
                    msg.sender, // msg.sender is predictable
                    block.difficulty, // can actually be manipulated by the miners!
                    block.timestamp // timestamp is predictable
                )
            )
        );
        fulfill(rn);

        // So we are not using VRF otherwise we will use requestId to store the address of user
        // Because fulfill function is then called by VRF not by the user so we will use this mapping there to take the address
        // bytest32 requestId = requestRandomness(keyhash, fee);
        // requestIdToSender[requestId] = msg.sender;
        return rn;
    }

    function fulfill(uint256 randomNumber) internal {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed); // Emitting the event that we assigned the mapping
        address owner = msg.sender; // So here msg.sender is not correct When we use VRF conusmer so here we will use mapping to get the owner address
        _safeMint(owner, newTokenId); // this will called only once for the unique token id
        // _setTokenURI(newTokenId, tokenURI); // This will be called many times with the token id
        tokenCounter++;
    }

    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        // _isApprovedOrOwner available from openzeppelin ERC721
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not the owner nor approved"
        );
        _setTokenURI(tokenId, tokenURI);
    }
}
