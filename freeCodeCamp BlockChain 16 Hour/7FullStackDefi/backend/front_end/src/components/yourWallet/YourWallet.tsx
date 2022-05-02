import React, { useState } from 'react';
import { Token } from '../Main';
import { Box } from "@material-ui/core";
import { TabContext, TabList, TabPanel } from "@material-ui/lab";
import { Tab } from "@material-ui/core";
import { WalletBalance } from "./WalletBalance";
import { StakeForm } from './StakeForm';
import { makeStyles } from "@material-ui/core";

interface YourWalletProps {
    supportedTokens: Array<Token>
}

const useStyles = makeStyles((theme) => ({
    tabContent: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: theme.spacing(4)
    },
    box: {
        backgroundColor: "white",
        borderRadius: "25px"
    },
    header: {
        color: "white",
    }
}))

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
    const classes = useStyles();

    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0);

    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue));
    }

    return (
        <Box>
            <h1 className={classes.header}>Your Wallet!</h1>
            <Box className={classes.box}>
                <TabContext value={selectedTokenIndex.toString()}>
                    <TabList onChange={handleChange} aria-label="stake from tabs">
                        {supportedTokens.map((token, index) => (
                            <Tab label={token.name} key={index} value={index.toString()} />
                        ))}
                    </TabList>
                    {supportedTokens.map((token, index) => (
                        // TabPanel will automatically show only that index which is active not shown other index
                        <TabPanel key={index} value={index.toString()}>
                            <h1>{token.name}</h1>
                            <div className={classes.tabContent}>
                                <WalletBalance token={supportedTokens[selectedTokenIndex]} />
                                <StakeForm token={supportedTokens[selectedTokenIndex]} />
                            </div>
                        </TabPanel>
                    ))}
                </TabContext>

            </Box>
        </Box>
    );
}