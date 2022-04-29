import React, { useState } from 'react';
import { Token } from '../Main';
import { Box } from "@material-ui/core";
import { TabContext, TabList, TabPanel } from "@material-ui/lab";
import { Tab } from "@material-ui/core";
import { WalletBalance } from "./WalletBalance";

interface YourWalletProps {

    supportedTokens: Array<Token>
}

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0);

    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue));
    }

    return (
        <Box>
            <h1>Your Wallet!</h1>
            <Box>
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
                            <div>
                                <WalletBalance token={token} />
                                {/* 2. a big stake button */}
                            </div>
                        </TabPanel>
                    ))}
                </TabContext>

            </Box>
        </Box>
    );
}