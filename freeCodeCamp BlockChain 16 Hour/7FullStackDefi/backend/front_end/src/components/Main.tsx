import { useEthers } from "@usedapp/core";
import HelperConfig from "../helper-config.json";
import networkMapping from '../chain-info/deployments/map.json';
import { constants } from "ethers";
import brownieConfig from '../brownie-config.json';
import { YourWallet } from "./yourWallet/YourWallet";
import { makeStyles } from "@material-ui/core";

export type Token = {
    image: string,
    address: string,
    name: string
}

const useStyles = makeStyles((theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4),
    }
}))

export const Main = () => {
    const classes = useStyles();
    // Show token values from the wallet
    // Get the address of different tokens
    // Get the balance of the users
    // Send the brownie-config to our `src` folder
    // Send the build folder

    const { chainId } = useEthers()
    // "suppressImplicitAnyIndexErrors": true and this line in your tsconfig.json file if there is error
    const networkName = chainId ? HelperConfig[chainId] : "development";
    console.log("Here is the CHAINID ", chainId);
    console.log(chainId);
    console.log(networkName);

    // We get the address of this token from our build because we deployed this contract/token
    const dappTokenAddres = chainId ? networkMapping[String(chainId)]["DappToken"][0] : constants.AddressZero;
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero;
    const fauTokenAddress = chainId ? brownieConfig["networks"][networkName]["fau_token"] : constants.AddressZero;

    const supportedTokens: Array<Token> = [
        {
            image: "/dapp.png",
            address: dappTokenAddres,
            name: "DAPP"
        },
        {
            image: "/weth.png",
            address: wethTokenAddress,
            name: "WETH"
        },
        {
            image: "/dai.png",
            address: fauTokenAddress,
            name: "DAI"
        }
    ];

    return (
        <>
            <h2 className={classes.title}>Dapp Token App</h2>
            <YourWallet supportedTokens={supportedTokens} />
        </>
    );
};
