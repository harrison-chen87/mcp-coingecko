"""CoinGecko API wrapper for MCP server."""

import os
import httpx
from typing import Optional, List, Dict, Any


class CoinGeckoClient:
    """Client for interacting with CoinGecko API."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize CoinGecko client with optional API key."""
        self.api_key = api_key or os.getenv("COINGECKO_API_KEY")
        self.headers = {}
        if self.api_key:
            self.headers["x-cg-demo-api-key"] = self.api_key

    async def get_coin_price(
        self,
        coin_ids: List[str],
        vs_currencies: List[str] = ["usd"],
        include_market_cap: bool = False,
        include_24h_vol: bool = False,
        include_24h_change: bool = False,
        include_last_updated: bool = False
    ) -> Dict[str, Any]:
        """
        Get current price of cryptocurrencies.

        Args:
            coin_ids: List of coin IDs (e.g., ["bitcoin", "ethereum"])
            vs_currencies: List of currencies to convert to (e.g., ["usd", "eur"])
            include_market_cap: Include market cap
            include_24h_vol: Include 24h volume
            include_24h_change: Include 24h price change
            include_last_updated: Include last updated timestamp

        Returns:
            Dictionary with price data
        """
        params = {
            "ids": ",".join(coin_ids),
            "vs_currencies": ",".join(vs_currencies),
            "include_market_cap": str(include_market_cap).lower(),
            "include_24hr_vol": str(include_24h_vol).lower(),
            "include_24hr_change": str(include_24h_change).lower(),
            "include_last_updated_at": str(include_last_updated).lower()
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/simple/price",
                params=params,
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_market_data(
        self,
        vs_currency: str = "usd",
        coin_ids: Optional[List[str]] = None,
        order: str = "market_cap_desc",
        per_page: int = 10,
        page: int = 1,
        sparkline: bool = False,
        price_change_percentage: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get market data for cryptocurrencies.

        Args:
            vs_currency: Target currency (e.g., "usd")
            coin_ids: Optional list of specific coin IDs to filter
            order: Sort order (market_cap_desc, volume_desc, id_asc, etc.)
            per_page: Number of results per page (max 250)
            page: Page number
            sparkline: Include sparkline 7d data
            price_change_percentage: Include price change % for periods (e.g., "1h,24h,7d")

        Returns:
            List of coin market data
        """
        params = {
            "vs_currency": vs_currency,
            "order": order,
            "per_page": min(per_page, 250),
            "page": page,
            "sparkline": str(sparkline).lower()
        }

        if coin_ids:
            params["ids"] = ",".join(coin_ids)

        if price_change_percentage:
            params["price_change_percentage"] = price_change_percentage

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/coins/markets",
                params=params,
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_historical_data(
        self,
        coin_id: str,
        vs_currency: str = "usd",
        days: int = 7,
        interval: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get historical market data for a cryptocurrency.

        Args:
            coin_id: Coin ID (e.g., "bitcoin")
            vs_currency: Target currency (e.g., "usd")
            days: Number of days of data (1, 7, 14, 30, 90, 180, 365, max)
            interval: Data interval (daily for days > 90, otherwise automatic)

        Returns:
            Dictionary with historical price, market cap, and volume data
        """
        params = {
            "vs_currency": vs_currency,
            "days": days
        }

        if interval:
            params["interval"] = interval

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/coins/{coin_id}/market_chart",
                params=params,
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def search_coins(self, query: str) -> Dict[str, Any]:
        """
        Search for cryptocurrencies.

        Args:
            query: Search query (coin name or symbol)

        Returns:
            Dictionary with search results including coins, exchanges, categories
        """
        params = {"query": query}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/search",
                params=params,
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_trending_coins(self) -> Dict[str, Any]:
        """
        Get trending cryptocurrencies.

        Returns:
            Dictionary with trending coins, NFTs, and categories
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/search/trending",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_coin_details(self, coin_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a cryptocurrency.

        Args:
            coin_id: Coin ID (e.g., "bitcoin")

        Returns:
            Dictionary with detailed coin information
        """
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "true",
            "developer_data": "false",
            "sparkline": "false"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/coins/{coin_id}",
                params=params,
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
