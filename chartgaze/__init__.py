"""ChartGaze Python SDK — thin HTTP client for api.chartgaze.live (MCP + REST)."""

from __future__ import annotations

__version__ = "0.1.1"

from typing import Any, Dict, List, Mapping, Optional, Union
from urllib.parse import quote

import json
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://api.chartgaze.live"


class ChartGazeError(Exception):
    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"HTTP {status_code}: {body[:300]}")


class ChartGaze:
    """Client for ChartGaze HTTP / MCP-backed market intelligence."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        oauth_token: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 60.0,
    ):
        token = (oauth_token or api_key or "").strip()
        if not token:
            raise ValueError("api_key or oauth_token is required")
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, body: Any = None) -> Any:
        data = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            self.base_url + path,
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8") or "null"
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise ChartGazeError(e.code, err_body) from e

    def list_tools(self) -> Any:
        return self._request("GET", "/mcp/tools")

    def call_tool(self, tool_name: str, tool_input: Optional[Mapping[str, Any]] = None) -> Any:
        q = quote(tool_name, safe="")
        return self._request("POST", f"/mcp/call?tool_name={q}", dict(tool_input or {}))

    def get_market_snapshot(self, symbol: str) -> Any:
        return self.call_tool("get_market_snapshot", {"symbol": symbol})

    def get_market_context(self, symbol: str, include_events: bool = True) -> Any:
        return self.call_tool(
            "get_market_context",
            {"symbol": symbol, "include_events": include_events},
        )

    def compare_markets(self, symbols: List[str]) -> Any:
        return self.call_tool("compare_markets", {"symbols": symbols})

    def get_historical_context(self, symbol: str, timestamp: str) -> Any:
        return self.call_tool(
            "get_historical_context",
            {"symbol": symbol, "timestamp": timestamp},
        )

    def get_economic_calendar_week(self) -> Any:
        return self.call_tool("get_economic_calendar_week", {})

    def get_trading_accounts(self) -> Any:
        return self.call_tool("get_trading_accounts", {})

    def propose_trade(
        self,
        account_id: str,
        symbol: str,
        side: str,
        volume: float,
        *,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        order_type: str = "market",
        entry_price: Optional[float] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Queue trade for Activity approval. Requires Review or Live mode. account_id required."""
        payload: Dict[str, Any] = {
            "account_id": account_id,
            "symbol": symbol,
            "side": side,
            "volume": volume,
            "order_type": order_type,
        }
        if stop_loss is not None:
            payload["stop_loss"] = stop_loss
        if take_profit is not None:
            payload["take_profit"] = take_profit
        if entry_price is not None:
            payload["entry_price"] = entry_price
        if comment:
            payload["comment"] = comment
        return self.call_tool("propose_trade", payload)

    def execute_trade(
        self,
        account_id: str,
        symbol: str,
        side: str,
        volume: float,
        *,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        order_type: str = "market",
        entry_price: Optional[float] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Immediate place — Live mode only. account_id required."""
        payload: Dict[str, Any] = {
            "account_id": account_id,
            "symbol": symbol,
            "side": side,
            "volume": volume,
            "order_type": order_type,
        }
        if stop_loss is not None:
            payload["stop_loss"] = stop_loss
        if take_profit is not None:
            payload["take_profit"] = take_profit
        if entry_price is not None:
            payload["entry_price"] = entry_price
        if comment:
            payload["comment"] = comment
        return self.call_tool("execute_trade", payload)

    def get_usage_summary(self) -> Any:
        return self._request("GET", "/usage/summary")

    def list_accounts(self) -> Any:
        return self._request("GET", "/accounts/list")


__all__ = ["ChartGaze", "ChartGazeError", "DEFAULT_BASE_URL", "__version__"]
