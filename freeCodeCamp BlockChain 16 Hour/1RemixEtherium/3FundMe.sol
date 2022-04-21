// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;
// we are using compiler version 0.6.6

// sometime v0.8 version error so change the version according to the compiler version
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
// this import uses Rinkbey test network not rinkbey 
// Remember this import from actual test network not vm so we need to deploy it on the inject web of Rinkbey network


contract FundMe {
    // this will solving overflow wrapping problem of large numbers but don't need in 0.8+ solidity
    using SafeMathChainlink for uint256; 
    
    // getting value by addresses // You can't use loop on mapping so in this case we use array for storing the values after that we will set them to zero in withdraw function
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner; // this will persist owner address

    // It will be executed whenever we will deploy this contract
    constructor() public {
        // so when someone deployed this contract whose address will be settled as the owner
        owner = msg.sender;
    }


    function fund() public payable {
        // Now let's set a threshhold that a user can send minimum 20$ 
        uint256 minimumUSD = 20 * 10 ** 18; // setting 20 Dollar for comparison

        // so it is like if value is greate then or equal to 50 dollar then go further otherwise stop the execution with the msg
        // msg.value (contains eth amount which is sent by user)
        require(getConverstionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");
        // what the ETH -> USD conversion rate


        // msg.sender (address) msg.value (value)    // Having two attributes
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender); // somebody funds multiple times it's redudant but for now it's okay
    }

    function getVersion() public view returns(uint256) {
        // ETH TO USD address we placed inside it
        // https://docs.chain.link/docs/ethereum-addresses/ (get this address from there)
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        // this have 8 decimal we are adding 10 more for make it as wei conversion to usd 
        // ETH TO USD 8 DECIMAL GWEI TO USD 18 DECIMAL for wei decimal places
        return uint256(answer * 10000000000); // parsing int256 to uint256
    }         

    // getting eth amount in USD according to ETH amount
    function getConverstionRate(uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice(); // getting etherium current 1ETH price 
        uint256 ethAmountInUSD = (ethPrice * ethAmount) / 1000000000000000000; // Dividing by 18 zeros to remove that decimal 18 values to get the exact to usd price
        return ethAmountInUSD;
    }

    modifier onlyOwner {
        // _; // means execute all the code of function then run require function
        require(msg.sender == owner, "You are not the owner of this contract!");
        _; // means execute after wards code
    }

    // 10000000000
    function withDraw() payable onlyOwner public {
        // Who ever call this withdraw function transfer all the money on this address

        // To avoid this use inside the function we will use modifier 
        // require(msg.sender == owner, "You are not the owner of this contract!");
        msg.sender.transfer(address(this).balance);

        for(uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;              
        }
        funders = new address[](0); // setting array to empty for now
    }


    
}

