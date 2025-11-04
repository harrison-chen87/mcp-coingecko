# CoinGecko MCP Server for Databricks

A Model Context Protocol (MCP) server that provides cryptocurrency price and market data from the CoinGecko API, deployed as a Databricks App.

## Overview

This MCP server enables AI agents and applications to access real-time and historical cryptocurrency data through standardized tools. It's designed to run on Databricks Apps with built-in authentication and scalable infrastructure.

## Features

### Available Tools

1. **get_coin_price** - Get current prices for cryptocurrencies
   - Real-time price data in multiple currencies
   - Market cap, 24h volume, and price change metrics
   - Support for multiple coins in a single request

2. **get_market_data** - Comprehensive market data for cryptocurrencies
   - Top coins by market cap or volume
   - Price change percentages (1h, 24h, 7d)
   - Sortable and paginated results

3. **get_historical_data** - Historical market data and price charts
   - Price, market cap, and volume history
   - Flexible time ranges (1 day to max history)
   - OHLC data for charting

4. **search_coins** - Search for cryptocurrencies
   - Find coins by name or symbol
   - Returns matching coins, exchanges, and categories

5. **get_trending_coins** - Currently trending cryptocurrencies
   - Based on CoinGecko search activity
   - Includes trending NFTs and categories

6. **get_coin_details** - Detailed information about specific coins
   - Comprehensive coin metadata
   - Links, descriptions, and community data

## Architecture

```
mcp-coingecko/
├── databricks.yml          # Databricks Asset Bundle configuration
├── src/
│   ├── app.yaml           # Databricks Apps runtime config
│   ├── requirements.txt   # Python dependencies
│   ├── server.py          # MCP server implementation
│   └── coingecko_tools.py # CoinGecko API wrapper
├── API_KEY_SETUP.txt      # Instructions for setting up API key
└── README.md
```

## Prerequisites

- Databricks workspace (Azure, AWS, or GCP)
- Databricks CLI installed and configured
- CoinGecko API key (free tier: 30 calls/min)
- Python 3.10+

## Setup

### 1. Configure CoinGecko API Key

See `API_KEY_SETUP.txt` for detailed instructions on adding your API key to Databricks secrets.

**Quick setup:**
```bash
# Create secret scope
databricks secrets create-scope coingecko

# Add API key
databricks secrets put-secret coingecko api_key
```

### 2. Deploy to Databricks

```bash
# Validate the bundle
databricks bundle validate

# Deploy the app
databricks bundle deploy

# Check deployment status
databricks apps list
```

### 3. Test in Databricks AI Playground

1. Navigate to Databricks AI Playground
2. Click "Add Tools" or "Connect MCP Server"
3. Select your deployed `mcp-coingecko` app
4. Start asking questions about cryptocurrency data!

## Usage Examples

### Example Queries in AI Playground

**Get Bitcoin Price:**
```
What's the current price of Bitcoin in USD?
```

**Compare Top Cryptocurrencies:**
```
Show me the top 10 cryptocurrencies by market cap
```

**Historical Analysis:**
```
Get the 30-day price history for Ethereum
```

**Search for Coins:**
```
Find all coins related to "layer 2"
```

**Trending Data:**
```
What are the trending cryptocurrencies right now?
```

## Local Development

### Test Locally

```bash
# Install dependencies
cd src
pip install -r requirements.txt

# Set environment variables
export COINGECKO_API_KEY="your_api_key_here"
export DATABRICKS_APP_PORT="8000"

# Run the server
python server.py
```

### Connect with Claude Desktop (Local Testing)

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "coingecko": {
      "command": "python",
      "args": ["/path/to/mcp-coingecko/src/server.py"],
      "env": {
        "COINGECKO_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Configuration

### app.yaml

Configures the Databricks App runtime:
- Command to start the server
- Environment variables (port, API key from secrets)

### databricks.yml

Defines the Databricks Asset Bundle:
- Workspace URL and deployment settings
- App resource configuration
- Source code path

## API Rate Limits

**Free Tier:**
- 30 calls per minute
- 1-5 minute data cache
- Access to 30 endpoints

**Pro Tier (if you upgrade):**
- Higher rate limits
- Faster data updates (30 sec cache)
- Access to 70+ endpoints

## Troubleshooting

### Deployment Issues

**Bundle validation fails:**
```bash
databricks bundle validate
```
Check for syntax errors in YAML files.

**App won't start:**
- Verify API key is set in Databricks secrets
- Check app logs: `databricks apps logs mcp-coingecko`

### API Issues

**Rate limit errors:**
- Implement caching in your queries
- Consider upgrading to CoinGecko Pro

**Authentication errors:**
- Verify secret scope and key names match app.yaml
- Ensure API key is valid

## Architecture Details

### MCP Protocol

This server uses the Model Context Protocol (MCP) standard:
- Server-Sent Events (SSE) transport
- Async tool execution
- JSON-RPC message format

### Databricks Integration

- **Apps Platform:** Handles infrastructure, scaling, and networking
- **Secrets:** Secure API key storage
- **Asset Bundles:** Version-controlled deployment configuration

## Contributing

To extend this server with additional tools:

1. Add new methods to `coingecko_tools.py` for API endpoints
2. Create corresponding `@mcp.tool()` functions in `server.py`
3. Test locally before deploying
4. Update this README with new tool documentation

## Resources

- [CoinGecko API Documentation](https://docs.coingecko.com/)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [Databricks Apps Documentation](https://docs.databricks.com/en/dev-tools/apps/)
- [Databricks Asset Bundles](https://docs.databricks.com/en/dev-tools/bundles/)

## License

MIT License - See LICENSE file for details

## Support

For issues related to:
- **CoinGecko API:** Contact CoinGecko support
- **Databricks Apps:** Refer to Databricks documentation or support
- **This MCP Server:** Open an issue in the repository

---

**Workspace:** https://<your-workspace-url>.azuredatabricks.net/
**Workspace ID:** <your-workspace-id>
