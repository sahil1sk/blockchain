import { Button, CircularProgress, Input, Snackbar } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import { useEthers, useTokenBalance, useNotifications } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { useEffect, useState } from "react";
import { Token } from "../Main";
import { useStakeTokens } from "../../hooks/useStakeTokens";
import { utils } from "ethers";

export interface StakeFormProps {
    token: Token,
}

export const StakeForm = ({ token }: StakeFormProps) => {
    const { image, address, name } = token;
    const { account } = useEthers();
    const tokenBalance = useTokenBalance(address, account);
    // Formatting the big decimal number remove extra 18 zeros
    const formattedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0;

    const { notifications } = useNotifications();

    const [amount, setAmount] = useState<number | string | Array<number | string>>(0);

    const hangleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === "" ? "" : Number(event.target.value);
        setAmount(newAmount);
        console.log(newAmount);
    }

    // Approve the erc20 token to this token contract
    const { approve, state } = useStakeTokens(address);
    const handleStakeSubmit = () => {
        const amountAsWei = utils.parseEther(amount.toString());
        return approve(amountAsWei.toString());
    }

    const isMinning = state.status === "Mining";
    const [showERC20ApproveSuccess, setERC20ApproveSuccess] = useState(false);
    const [showStakeTokenSuccess, setStakeTokenSuccess] = useState(false);

    useEffect(() => {
        if (notifications.filter(n => n.type === "transactionSucceed" && n.transactionName === "Approve ERC20 transfer").length > 0) {
            console.log("Approve ERC20 transfer");
            setERC20ApproveSuccess(true);
            setStakeTokenSuccess(false);
        }
        // if (notifications.filter(n => n.type === "transactionFailed" && n.transactionName === "Approve ERC20 transfer").length > 0) {
        if (notifications.filter(n => n.type === "transactionSucceed" && n.transactionName === "Stake Tokens").length > 0) {
            console.log("Stake Tokens");
            setERC20ApproveSuccess(false);
            setStakeTokenSuccess(true);
        }

    }, [notifications, showERC20ApproveSuccess, showStakeTokenSuccess]);

    const handleCloseSnack = () => {
        setERC20ApproveSuccess(false);
        setStakeTokenSuccess(false);
    }

    return (
        <>
            <div>
                <Input onChange={hangleInputChange} />
                <Button
                    onClick={handleStakeSubmit}
                    color="primary"
                    size="large"
                    disabled={isMinning}
                >
                    {isMinning ? <CircularProgress size={26} /> : "Stake!!"}
                </Button>
            </div>
            <Snackbar
                open={showERC20ApproveSuccess}
                autoHideDuration={5000}
                onClose={handleCloseSnack}
            >
                <Alert onClose={handleCloseSnack} severity="success"> ERC-20 token transfer approved! - Now approve the 2nd transaction</Alert>
            </Snackbar>
            <Snackbar
                open={showStakeTokenSuccess}
                autoHideDuration={5000}
                onClose={handleCloseSnack}
            >
                <Alert onClose={handleCloseSnack} severity="success">Token Staked!</Alert>
            </Snackbar>
        </>
    )
}