import { Button, Input } from "@material-ui/core";
import { useEthers, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { useState } from "react";
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

    const [amount, setAmount] = useState<number | string | Array<number | string>>(0);

    const hangleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === "" ? "" : Number(event.target.value);
        setAmount(newAmount);
        console.log(newAmount);
    }

    // Approve the erc20 token to this token contract
    const { approve, approveERc20State } = useStakeTokens(address);
    const handleStakeSubmit = () => {
        const amountAsWei = utils.parseEther(amount.toString());
        return approve(amountAsWei.toString());
    }

    return (
        <>
            <Input onChange={hangleInputChange} />
            <Button
                onClick={handleStakeSubmit}
                color="primary"
                size="large"
            >Stake!!</Button>
        </>
    )
}