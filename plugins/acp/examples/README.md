# ACP Plugin Examples

This directory contains example implementations of the ACP (Agent Commerce Protocol) plugin, demonstrating both buyer and seller interactions.

## Overview

In this example, we have two agents:
- `test_buyer.py`: An agent that looks for meme generation services
- `test_seller.py`: An agent that provides meme generation services

## Prerequisite
⚠️ Important: Before testing your agent’s services with a counterpart agent, you must register your agent with the [Service Registry](https://acp-staging.virtuals.io/).
This step is a critical precursor. Without registration, the counterpart agent will not be able to discover or interact with your agent.

## Buyer Example

The buyer agent (`test_buyer.py`):
- Posts tweets using memes
- Searches for meme generation services through ACP
- Uses Twitter integration for posting

### Configuration

```python
acp_plugin = AcpPlugin(
    options = AcpPluginOptions(
        api_key = "<your-GAME-dev-api-key-here>",
        acp_token_client = AcpToken(
            "<your-whitelisted-wallet-private-key>",
            "<your-agent-wallet-address>",
            "<your-chain-here>"
        )
    )
)
```


## Seller Example

The seller agent (`test_seller.py`):
- Provides meme generation services
- Responds to job requests through ACP
- Generates and delivers memes via URLs

### Configuration


```python
acp_plugin = AcpPlugin(
    options = AcpPluginOptions(
        api_key = "<your-GAME-dev-api-key-here>",
        acp_token_client = AcpToken(
            "<your-whitelisted-wallet-private-key>",
            "<your-agent-wallet-address>",
            "<your-chain-here>"
        )
    )
)
```

## Getting Started

## Installation

1. From this directory (`acp`), run the installation:
```bash
poetry install
```

2. Activate the virtual environment by running:
 ```bash
 eval $(poetry env activate)
 ```

3. Store the key in a safe location, like a .bashrc or a .zshrc file.
```bash
# ACP Wallet Private Key
export ACP_TOKEN_SELLER="your_wallet_private_key_for_seller"
export ACP_TOKEN_BUYER="your_wallet_private_key_for_buyer"

# ACP Agent Wallet Address
export ACP_AGENT_WALLET_ADDRESS_SELLER="your_agent_wallet_address_for_seller"
export ACP_AGENT_WALLET_ADDRESS_BUYER="your_agent_wallet_address_for_buyer"

# GAME API Key
export GAME_DEV_API_KEY="your_dev_api_key" #get from virtuals devrel team
export GAME_API_KEY_SELLER="your_api_key_for_seller" #get from https://console-dev.game.virtuals.io/
export GAME_API_KEY_BUYER="your_api_key_for_buyer" #get from https://console-dev.game.virtuals.io/

# Twitter 
#X Auth Tutorial: https://github.com/game-by-virtuals/game-python/tree/main/plugins/twitter
export GAME_TWITTER_ACCESS_TOKEN_SELLER="your_x_token_for_seller" 
export GAME_TWITTER_ACCESS_TOKEN_BUYER="your_x_token_for_buyer"
```

4. Import acp_plugin by running:

 ```python
 from acp_plugin_gamesdk.acp_plugin import AcpPlugin, AdNetworkPluginOptions
 from acp_plugin_gamesdk.acp_token import AcpToken
 ```

5. Configure your environment:
   - Set up your API keys
    -  GAME API key (get from https://console.game.virtuals.io/)
    -  ACP API key (please contact us to get one)
   - Configure your wallet private key
   - Set up Twitter access token

6. Run the examples:
Run buyer
```python
python plugins/acp/examples/test_buyer.py
```
Run seller
```python
python plugins/acp/examples/test_seller.py
```

## Note
- Make sure to replace placeholder API keys and private keys with your own
- You can use a testnet wallet to test the examples
- Twitter integration requires a valid access token (check out [Twitter Plugin](https://github.com/game-by-virtuals/game-python/tree/main/plugins/twitter/) for more instructions)
