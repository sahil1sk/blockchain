import React from 'react';
import { getDefaultProvider } from 'ethers'

import { ChainId, DAppProvider, DEFAULT_SUPPORTED_CHAINS, Config, Kovan } from '@usedapp/core';
import { Header } from './components/Header';
import { Container } from '@material-ui/core';
import { Main } from './components/Main';

const config: Config = {
  readOnlyChainId: Kovan.chainId,
  readOnlyUrls: {
    [Kovan.chainId]: getDefaultProvider('kovan'),
  },
}

function App() {
  return (
    <DAppProvider
      config={config}
    // config={{   // We are only supporting kovan here
    //   // supportedChains: [ChainId.Kovan], // [ChainId.Kovan, ChainId.Rinkeby, 1337]
    //   networks: DEFAULT_SUPPORTED_CHAINS
    // }}
    >
      <Header />
      <Container maxWidth='md'>
        <Main />
      </Container>
    </DAppProvider>
  );
}

export default App;
