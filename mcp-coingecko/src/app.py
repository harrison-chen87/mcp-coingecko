"""CoinGecko MCP Server for Databricks Apps."""

import os
import json
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from coingecko_tools import CoinGeckoClient

# Initialize FastMCP server
mcp = FastMCP("coingecko")

# Initialize CoinGecko client
coingecko = CoinGeckoClient()


@mcp.tool()
async def get_coin_price(
    coin_ids: List[str],
    vs_currencies: List[str] = ["usd"],
    include_market_cap: bool = True,
    include_24h_vol: bool = True,
    include_24h_change: bool = True
) -> str:
    """
    Get current price of cryptocurrencies.

    Args:
        coin_ids: List of coin IDs (e.g., ["bitcoin", "ethereum"])
        vs_currencies: List of currencies to convert to (default: ["usd"])
        include_market_cap: Include market cap data (default: True)
        include_24h_vol: Include 24h volume data (default: True)
        include_24h_change: Include 24h price change data (default: True)

    Returns:
        JSON string with current price data for requested cryptocurrencies

    Example:
        get_coin_price(["bitcoin", "ethereum"], ["usd", "eur"])
    """
    try:
        result = await coingecko.get_coin_price(
            coin_ids=coin_ids,
            vs_currencies=vs_currencies,
            include_market_cap=include_market_cap,
            include_24h_vol=include_24h_vol,
            include_24h_change=include_24h_change,
            include_last_updated=True
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_market_data(
    vs_currency: str = "usd",
    coin_ids: Optional[List[str]] = None,
    per_page: int = 10,
    page: int = 1,
    order: str = "market_cap_desc"
) -> str:
    """
    Get comprehensive market data for cryptocurrencies.

    Args:
        vs_currency: Target currency (default: "usd")
        coin_ids: Optional list of specific coin IDs to filter
        per_page: Number of results per page (max 250, default: 10)
        page: Page number (default: 1)
        order: Sort order - options: market_cap_desc, volume_desc, id_asc, id_desc (default: market_cap_desc)

    Returns:
        JSON string with market data including price, market cap, volume, and more

    Example:
        get_market_data(vs_currency="usd", per_page=5, order="volume_desc")
    """
    try:
        result = await coingecko.get_market_data(
            vs_currency=vs_currency,
            coin_ids=coin_ids,
            order=order,
            per_page=per_page,
            page=page,
            price_change_percentage="1h,24h,7d"
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_historical_data(
    coin_id: str,
    vs_currency: str = "usd",
    days: int = 7
) -> str:
    """
    Get historical market data for a cryptocurrency.

    Args:
        coin_id: Coin ID (e.g., "bitcoin", "ethereum")
        vs_currency: Target currency (default: "usd")
        days: Number of days of historical data (1, 7, 14, 30, 90, 180, 365, or "max", default: 7)

    Returns:
        JSON string with historical price, market cap, and volume data with timestamps

    Example:
        get_historical_data("bitcoin", "usd", 30)
    """
    try:
        result = await coingecko.get_historical_data(
            coin_id=coin_id,
            vs_currency=vs_currency,
            days=days
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def search_coins(query: str) -> str:
    """
    Search for cryptocurrencies by name or symbol.

    Args:
        query: Search query (coin name or symbol, e.g., "bitcoin" or "BTC")

    Returns:
        JSON string with search results including coins, exchanges, and categories

    Example:
        search_coins("ethereum")
    """
    try:
        result = await coingecko.search_coins(query=query)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_trending_coins() -> str:
    """
    Get currently trending cryptocurrencies.

    Returns:
        JSON string with trending coins, NFTs, and categories based on search activity

    Example:
        get_trending_coins()
    """
    try:
        result = await coingecko.get_trending_coins()
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_coin_details(coin_id: str) -> str:
    """
    Get detailed information about a specific cryptocurrency.

    Args:
        coin_id: Coin ID (e.g., "bitcoin", "ethereum", "cardano")

    Returns:
        JSON string with comprehensive coin details including description, links, market data, and community data

    Example:
        get_coin_details("bitcoin")
    """
    try:
        result = await coingecko.get_coin_details(coin_id=coin_id)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


# Create the Streamable HTTP MCP app (required for Databricks Apps)
mcp_app = mcp.streamable_http_app()

# Wrap in FastAPI with lifespan management
app = FastAPI(
    title="CoinGecko MCP Server",
    description="MCP server for CoinGecko cryptocurrency data",
    lifespan=lambda _: mcp.session_manager.run(),
)


# Add a homepage route before mounting MCP app
@app.get("/", response_class=HTMLResponse)
async def homepage():
    """Landing page showing server status and available tools."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CoinGecko MCP Server</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                line-height: 1.6;
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .status {
                display: inline-block;
                background: #10b981;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: bold;
                margin-top: 10px;
            }
            .content {
                padding: 40px;
            }
            .section {
                margin-bottom: 30px;
            }
            .section h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.5em;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .tool-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .tool-card {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 20px;
                transition: all 0.3s;
            }
            .tool-card:hover {
                border-color: #667eea;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
                transform: translateY(-2px);
            }
            .tool-name {
                font-weight: bold;
                color: #667eea;
                font-size: 1.1em;
                margin-bottom: 8px;
            }
            .tool-desc {
                color: #666;
                font-size: 0.95em;
            }
            .info-box {
                background: #f3f4f6;
                border-left: 4px solid #667eea;
                padding: 15px 20px;
                border-radius: 4px;
                margin: 15px 0;
            }
            .info-box code {
                background: #e5e7eb;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }
            .footer {
                text-align: center;
                padding: 20px;
                background: #f9fafb;
                color: #666;
                font-size: 0.9em;
            }
            .endpoint {
                background: #1f2937;
                color: #10b981;
                padding: 15px;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                margin: 10px 0;
                overflow-x: auto;
            }
            .badge {
                display: inline-block;
                background: #ddd6fe;
                color: #5b21b6;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.85em;
                font-weight: 600;
                margin-right: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🦎 CoinGecko MCP Server</h1>
                <p style="font-size: 1.2em; margin-top: 10px;">Model Context Protocol for Cryptocurrency Data</p>
                <div class="status">✅ Server Running</div>
            </div>

            <div class="content">
                <div class="section">
                    <h2>📡 MCP Endpoint</h2>
                    <p>Connect your MCP client to this Streamable HTTP endpoint:</p>
                    <div class="endpoint">/api/mcp/</div>
                    <div class="info-box">
                        <strong>How to connect:</strong> Add this server to Databricks AI Playground by selecting
                        <code>mcp-coingecko</code> from the available MCP servers.
                    </div>
                </div>

                <div class="section">
                    <h2>🛠️ Available Tools</h2>
                    <div class="tool-grid">
                        <div class="tool-card">
                            <div class="tool-name">get_coin_price</div>
                            <div class="tool-desc">Get real-time cryptocurrency prices with market data</div>
                        </div>
                        <div class="tool-card">
                            <div class="tool-name">get_market_data</div>
                            <div class="tool-desc">Market rankings, volume, and price changes</div>
                        </div>
                        <div class="tool-card">
                            <div class="tool-name">get_historical_data</div>
                            <div class="tool-desc">Historical price charts and OHLCV data</div>
                        </div>
                        <div class="tool-card">
                            <div class="tool-name">search_coins</div>
                            <div class="tool-desc">Search cryptocurrencies by name or symbol</div>
                        </div>
                        <div class="tool-card">
                            <div class="tool-name">get_trending_coins</div>
                            <div class="tool-desc">Currently trending cryptocurrencies</div>
                        </div>
                        <div class="tool-card">
                            <div class="tool-name">get_coin_details</div>
                            <div class="tool-desc">Detailed coin information and metadata</div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>💡 Example Queries</h2>
                    <div class="info-box">
                        <p>Try these questions in Databricks AI Playground:</p>
                        <ul style="margin-left: 20px; margin-top: 10px;">
                            <li>"What's the current price of Bitcoin?"</li>
                            <li>"Show me the top 10 cryptocurrencies by market cap"</li>
                            <li>"Get 7-day price history for Ethereum"</li>
                            <li>"What are the trending cryptocurrencies?"</li>
                        </ul>
                    </div>
                </div>

                <div class="section">
                    <h2>ℹ️ Server Information</h2>
                    <p>
                        <span class="badge">Protocol</span> MCP Streamable HTTP<br>
                        <span class="badge">Data Source</span> CoinGecko API<br>
                        <span class="badge">Rate Limit</span> 30 calls/min (Free Tier)<br>
                        <span class="badge">Platform</span> Databricks Apps
                    </p>
                </div>
            </div>

            <div class="footer">
                <p>Powered by FastMCP and CoinGecko API | Deployed on Databricks Apps</p>
                <p style="margin-top: 5px;">
                    <a href="/docs" style="color: #667eea; text-decoration: none;">API Documentation</a> |
                    <a href="/openapi.json" style="color: #667eea; text-decoration: none;">OpenAPI Schema</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


# Mount the MCP app at /api/mcp (not at root)
app.mount("/api/mcp", mcp_app)


if __name__ == "__main__":
    # For local testing
    import uvicorn
    port = int(os.getenv("DATABRICKS_APP_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
