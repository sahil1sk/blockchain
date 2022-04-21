// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

// we are using compiler version 0.6.6

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol"; // For getting ethereum latest price from outside the BC in decentralized way
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol"; // for using safe math for big calculations
import "@openzeppelin/contracts/access/Ownable.sol"; // for only owner modifiers
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol"; // for getting random number from outside the BC in decentralized way

// onlyOwner and Ownable comes from import

/*
    Search Like Aggregator Contract addreses chainlink docs

    // These all are different according to networks like for Rinkeby, Mainnet others are there
    // You will get all these addresses from chainlink docs
    
    // You will get this address from chainlink docs AggregatorV3Interface according to the network you want
    address _priceFeedAddress,

    // You will get this address from chainlink docs Link Token Contracts
    address _link,
    

    // You will get this address from chainlink docs VRFConsumerBase according to the network you want
    address _vrfCordinator,
    uint256 _fee,
    bytes32 _keyhash
*/

contract Lottery is VRFConsumerBase, Ownable {
    // this will solving overflow wrapping problem of large numbers but don't need in 0.8+ solidity
    using SafeMathChainlink for uint256;

    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;

    uint256 public usdEntryFee;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lotteryState;

    AggregatorV3Interface public ethUsdPriceFeed;

    uint256 public fee;
    bytes32 public keyhash;

    // events just like printing but uses very less gas than storing a variable
    // event RequestedRandomness(bytes32 requestId);
    event RequestedRandomness(uint256 requestId);

    // In java we using super to use constructor of parent class
    // In solidity we add after public and passes the variables in this
    // way getting from our consturctor and passing to interface consturctor

    constructor(
        address _priceFeedAddress,
        address _vrfCordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCordinator, _link) {
        usdEntryFee = 20 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lotteryState = LOTTERY_STATE.CLOSED;

        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // 20$ minimum
        require(lotteryState == LOTTERY_STATE.OPEN, "Lottery is closed");
        require(msg.value >= getEnteranceFee(), "Not enough ETH!");
        players.push(msg.sender);
    }

    function getEnteranceFee() public view returns (uint256) {
        (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = ethUsdPriceFeed.latestRoundData();

        // we have an answer in 8 digit decimal so we adding 10 more digits decimal
        // answer * (10**10)
        uint256 adjustedPrice = uint256(answer) * 10000000000;

        // $20, Ether price  // To get decimal we multiplied by some big number
        // (20 * 10**18) / 2000
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    // onlyOwner comes from onlyOwner import
    function startLottery() public onlyOwner {
        require(
            lotteryState == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery"
        );
        lotteryState = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // uint256(
        //     keccak256(
        //         abi.encodePacked(
        //             nonce, // nonce is preditable (aka, transaction number)
        //             msg.sender, // msg.sender is predictable
        //             block.difficulty, // can actually be manipulated by the miners!
        //             block.timestamp // timestamp is predictable
        //         )
        //     )
        // ) % players.length;
        lotteryState = LOTTERY_STATE.CALCULATING_WINNER;

        // Requesting Random number from interface function
        // so then automatically aftersome secords in response of this
        // VRFConsumerBase.sol will call the fulfillRandomness function
        // bytes32 requestId = requestRandomness(keyhash, fee);
        // emit RequestedRandomness(requestId);

        // For now we use this approach to calculate winner Because our Link Token Contract is in-compatible with this version
        // But this is not the secure method
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
        emit RequestedRandomness(rn);
        chooseWinner(rn);
    }

    // this we deploy for closing the lottery
    function chooseWinner(uint256 _randomness) internal {
        require(
            lotteryState == LOTTERY_STATE.CALCULATING_WINNER,
            "Lottery is not calculating winner"
        );
        require(_randomness > 0, "Random not found!");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];

        // Transfering all the balance of this contract to the winner
        recentWinner.transfer(address(this).balance);

        // Reset
        players = new address payable[](0);
        lotteryState = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }

    // This function is called by VRFConsumerBase
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lotteryState == LOTTERY_STATE.CALCULATING_WINNER,
            "Lottery is not calculating winner"
        );
        require(_randomness > 0, "Random not found!");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];

        // Transfering all the balance of this contract to the winner
        recentWinner.transfer(address(this).balance);

        // Reset
        players = new address payable[](0);
        lotteryState = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
