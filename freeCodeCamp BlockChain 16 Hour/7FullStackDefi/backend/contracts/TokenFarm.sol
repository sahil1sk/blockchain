// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    // stake tokens
    // unStake tokens
    // issueTokens          (Issue rewards)
    // addAllowedTokens     (add more tokens)
    // getEthValue

    // mapping token address -> staker address -> amount
    mapping(address => mapping(address => uint256)) public stakingBalance; // for setting the stake balance of the token of user address
    mapping(address => uint256) public uniqueTokenStaked; // for maintain the uniqueness of stakers array and also for counting how many unique tokens a user have
    mapping(address => address) public tokenPriceFeedMapping; // token price feed mapping  token address and price feed address from where we will get the price data (LIKE ETH/USD => Eth token address address and price feed address from where we get the eth value)
    address[] public stakers; // Unique stakers array (this array uniqueness is maintained by uniqueTokenStaked mapping)
    address[] public allowedTokens; // Allowed tokens array means which tokens are allowed to staked
    IERC20 public dappToken; // Dapp token contract address

    constructor(address _dappTokenAddress) {
        dappToken = IERC20(_dappTokenAddress);
    }

    // Setting different token address with it's price feed (After for using with V3 Aggregator)
    function setPriceFeedContract(address _token, address _priceeFeed)
        public
        onlyOwner
    {
        tokenPriceFeedMapping[_token] = _priceeFeed;
    }

    // So we are doing how much total value user has staked on this platform we will issue them equilent amount as award
    function issueToken() public onlyOwner {
        for (uint256 i = 0; i < stakers.length; i++) {
            address recipient = stakers[i];
            uint256 userTotalValue = getUserTotalValue(recipient);
            // Basically here we ASSUMED our DAPP token value equals to ETH value
            dappToken.transfer(recipient, userTotalValue);
        }
    }

    function getUserTotalValue(address _user) public view returns (uint256) {
        uint256 totalValue = 0;
        require(uniqueTokenStaked[_user] > 0, "No tokens staked for this user");
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            totalValue =
                totalValue +
                getUserSingleTokenValue(_user, allowedTokens[i]);
        }
        return totalValue;
    }

    // get the value of a single token by converting from decimals to real
    function getUserSingleTokenValue(address _user, address _token)
        public
        view
        returns (uint256)
    {
        if (uniqueTokenStaked[_user] <= 0) {
            return 0;
        }
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        // Because eth price has some decimal values so we need to convert it to real by dividing it by 10^decimals
        // stakingBalance[_token][_user] (total token amount * amount) // if zero amount there then amount will be sent zero for that token value
        return (stakingBalance[_token][_user] * price) / (10**decimals);
    }

    // get the 1 token value from the real world using V3 Aggregator
    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        // priceFeedAddress
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals()); // getting decimals of that pricefeed value
        return (uint256(price), decimals);
    }

    // Staking tokens
    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be greater than 0");
        require(tokenIsAllowed(_token), "Token is not allowed");
        // Send token from Msg.sender to this contract
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        updateUniqueTokenStaked(msg.sender, _token);
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;

        // Just for filling the tokens staked address so that we know who staked the tokens
        // for remove duplicaly we used this approach so that if uniqueToken values goes above means this person is already in our list
        if (uniqueTokenStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function updateUniqueTokenStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokenStaked[_user] = uniqueTokenStaked[_user] + 1;
        }
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public view returns (bool) {
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == _token) {
                return true;
            }
        }
        return false;
    }

    function unstakeTokens(address _token) public {
        uint256 balance = stakingBalance[_token][msg.sender];
        require(
            balance > 0,
            "No tokens staked for this user - Staking balance can't be 0"
        );
        // Send token from this contract to Msg.sender
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokenStaked[msg.sender] = uniqueTokenStaked[msg.sender] - 1;

        // remove from stakers array
        if (uniqueTokenStaked[msg.sender] == 0) {
            uint256 selectedIndex = 0;
            for (uint256 i = 0; i < stakers.length; i++) {
                if (stakers[i] == msg.sender) {
                    selectedIndex = i;
                }
            }
            delete stakers[selectedIndex];
        }
    }
}
