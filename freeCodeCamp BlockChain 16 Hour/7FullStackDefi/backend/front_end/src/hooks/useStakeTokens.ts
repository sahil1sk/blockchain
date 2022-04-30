import { useContractFunction, useEthers } from "@usedapp/core";
import { constants, utils } from "ethers";
import { Contract } from "@ethersproject/contracts";
import TokenFarm from "../chain-info/contracts/TokenFarm.json";
import IERC20 from "../chain-info/contracts/dependencies/OpenZeppelin/openzeppelin-contracts@4.2.0/IERC20.json";
import networkMapping from '../chain-info/deployments/map.json';
import { useEffect, useState } from "react";

export const useStakeTokens = (tokenAddress: string) => {
    // address, abi, chainId
    const { chainId } = useEthers();
    const { abi } = TokenFarm;
    // [0] means fetch latest one upper index
    const tokenFarmAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero;
    const tokenFarmInterface = new utils.Interface(abi);
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface);

    const erce20ABI = IERC20.abi;
    const erc20Interface = new utils.Interface(erce20ABI)
    const erc20Contract = new Contract(tokenAddress, erc20Interface);

    // For approving request to tokenFarm to use that much amount
    const { send: approveERc20Send, state: approveERc20State } = useContractFunction(erc20Contract, "approve", { transactionName: "Approve ERC20 transfer" });
    // So here our ERC20 Contract (which is from our token address) is approving the TokenFarm Contract to use the amount 
    const approve = (amount: string) => {
        setAmountToStake(amount);
        return approveERc20Send(tokenFarmAddress, amount);
    }

    const { send: stakeSend, state: stakeState } = useContractFunction(tokenFarmContract, "stakeTokens", { transactionName: "Stake Tokens" });
    // In this we will set the amount which we are staking
    const [amountToStake, setAmountToStake] = useState("0");

    // approveERc20State (This will trigger or change If we approve the Erc20Send Request)
    // when this trigger our useEffect will also triggered
    useEffect(() => {
        console.log("inside use effect");
        if (approveERc20State.status === "Success") {
            console.log("inside use effect if");
            stakeSend(amountToStake, tokenAddress);
        }
    }, [approveERc20State, amountToStake, tokenAddress]);


    return { approve, approveERc20State };

}


