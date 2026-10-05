# ChartGaze by TrainFlow AI — Python SDK

**ChartGaze** is the market-intelligence MCP / SDK from **[TrainFlow AI](https://www.trainflow.dev)** — give any AI live multi-TF structure, news, and your trading accounts.

> **Want the AI to trade for you?** ChartGaze is context + accounts.  
> For full autonomous scan → alert → execute on MT4 / MT5 / cTrader / crypto, use **[TrainFlow](https://www.trainflow.dev)** (Nexus / Hunter).  
> Same family: [chartgaze.live](https://chartgaze.live) · [trainflow.dev](https://www.trainflow.dev)

| | |
|---|---|
| Product | ChartGaze by TrainFlow AI |
| Site | https://chartgaze.live |
| Org | https://github.com/TrainFlow-AI |
| Autonomous trading | https://www.trainflow.dev |
| License | MIT |

---

## Overview

The **ChartGaze by TrainFlow AI** Python SDK lets you wire Claude, ChatGPT, custom agents, and apps into live market structure, economic events, and connected trading accounts (MT4 / MT5 / cTrader / crypto).

ChartGaze = **eyes** for your AI. For **hands** (full autonomous execution desks), go to **[TrainFlow](https://www.trainflow.dev)**.

### Key Use Cases

- **AI + MCP**: Feed any agent ChartGaze market context from Python
- **Research Tools**: Backtest and investigate with historical as-of context
- **Broker / account apps**: Connect MT4, MT5, cTrader, crypto into your stack
- **Hand-off to TrainFlow**: Prototype with ChartGaze, run autonomy on TrainFlow

---

## Installation

```bash
pip install chartgaze
```

Or install from source:

```bash
git clone https://github.com/TrainFlow-AI/chartgaze-python-sdk.git
cd python-sdk
pip install -e .
```

**Requirements**: Python 3.8+, `requests`, `python-dotenv`

---

## Quick Start

### 1. Basic Market Query

```python
from chartgaze import ChartGaze

# Initialize client
tg = ChartGaze(api_key="cg_pk_live_...")

# Get current market state
snapshot = tg.get_market_snapshot("EURUSD")
print(f"EURUSD: {snapshot.price} (bid: {snapshot.bid}, ask: {snapshot.ask})")

# Get multi-timeframe context
context = tg.get_market_context("XAUUSD")
print(f"Trend: {context.daily.trend}")
print(f"Structure: {context.hourly.structure}")
```

### 2. Account Integration

```python
# List connected accounts
accounts = tg.get_trading_accounts()
for account in accounts:
    print(f"{account.broker} - {account.platform}: {account.currency}")

# Get positions
positions = tg.get_positions(account_id=accounts[0].id)
for pos in positions:
    print(f"{pos.symbol}: {pos.side} {pos.volume} @ {pos.entry_price}")

# Get account info
info = tg.get_account_info(account_id=accounts[0].id)
print(f"Balance: ${info.balance} | Equity: ${info.equity}")
```

### 3. Market Analysis

```python
# Historical context (time machine)
historical = tg.get_historical_context(
    symbol="BTC/USD",
    timestamp="2026-09-15T14:30:00Z",
    lookback_minutes=60
)
print(f"BTC at 14:30: ${historical.price}")
print(f"Next 30 minutes: {historical.forward_context}")

# Compare markets
comparison = tg.compare_markets(
    symbols=["EURUSD", "GBPUSD", "DXY"],
    analysis_type="correlation"
)
print(comparison.relationships)

# Get events
events = tg.get_market_events(symbol="XAUUSD", hours_back=24)
for event in events:
    print(f"{event.time}: {event.name} (impact: {event.impact})")
```

### 4. Trading (Optional)

```python
# Enable trading in your account settings first
# Then:

# Propose a trade (review before execution)
proposal = tg.propose_trade(
    account_id="acct_123",
    symbol="EURUSD",
    side="BUY",
    volume=1.0,
    stop_loss=1.0800,
    take_profit=1.0920
)
print(f"Proposal ID: {proposal.id} - awaiting approval")

# Execute a trade (if you have trading.execute scope)
trade = tg.execute_trade(
    account_id="acct_123",
    symbol="EURUSD",
    side="BUY",
    volume=1.0,
    order_type="market",
    stop_loss=1.0800,
    take_profit=1.0920
)
print(f"Trade executed: {trade.id} @ {trade.execution_price}")

# Modify/close positions
tg.modify_position(
    account_id="acct_123",
    position_id="pos_456",
    stop_loss=1.0810,
    take_profit=1.0930
)

tg.close_position(account_id="acct_123", position_id="pos_456")
```

---

## Authentication

### API Key (Recommended for Scripts/Bots)

```python
from chartgaze import ChartGaze

# Use environment variable
import os
api_key = os.getenv("CHARTGAZE_API_KEY")
tg = ChartGaze(api_key=api_key)
```

### OAuth Token (For User-Facing Apps)

```python
from chartgaze.auth import OAuthClient

# During app initialization
oauth = OAuthClient(
    client_id="cg_client_123",
    client_secret="cg_secret_456"
)

# Get authorization URL
auth_url = oauth.get_authorization_url(
    scopes=["market.read", "portfolio.read", "trading.execute"]
)
print(f"Visit: {auth_url}")

# After user authorizes, exchange code for token
token = oauth.exchange_code(code="auth_code_from_callback")

# Create ChartGaze client with token
tg = ChartGaze(oauth_token=token)
```

---

## Async Support

For high-performance applications:

```python
import asyncio
from chartgaze.async_client import ChartGazeAsync

async def main():
    tg = ChartGazeAsync(api_key="cg_pk_live_...")
    
    # Fetch multiple snapshots concurrently
    symbols = ["EURUSD", "GBPUSD", "XAUUSD"]
    tasks = [tg.get_market_snapshot(s) for s in symbols]
    snapshots = await asyncio.gather(*tasks)
    
    for snapshot in snapshots:
        print(f"{snapshot.symbol}: {snapshot.price}")

asyncio.run(main())
```

---

## Error Handling

```python
from chartgaze import ChartGaze
from chartgaze.exceptions import (
    ChartGazeError,
    AuthenticationError,
    PermissionError,
    RateLimitError,
    NotFoundError
)

tg = ChartGaze(api_key="cg_pk_live_...")

try:
    snapshot = tg.get_market_snapshot("INVALID")
except NotFoundError:
    print("Symbol not found")
except PermissionError:
    print("You don't have permission for this operation")
except RateLimitError:
    print("Rate limit exceeded. Retry after:", e.retry_after)
except ChartGazeError as e:
    print(f"Error: {e.code} - {e.message}")
```

---

## Advanced: Autonomous Agent Example

```python
from chartgaze import ChartGaze
from datetime import datetime, timedelta

class MarketAgent:
    def __init__(self, api_key: str, account_id: str):
        self.tg = ChartGaze(api_key=api_key)
        self.account_id = account_id
    
    def analyze_and_trade(self, symbol: str):
        """Autonomous trading logic"""
        
        # 1. Get market context
        context = self.tg.get_market_context(symbol)
        
        # 2. Check account
        account = self.tg.get_account_info(self.account_id)
        if account.free_margin < 1000:
            print("Insufficient margin")
            return
        
        # 3. Decide
        if (context.daily.trend == "bullish" and 
            context.hourly.structure == "higher_high"):
            
            # 4. Execute
            trade = self.tg.execute_trade(
                account_id=self.account_id,
                symbol=symbol,
                side="BUY",
                volume=self._calculate_position_size(account),
                stop_loss=context.daily.support,
                take_profit=context.daily.resistance
            )
            print(f"Trade opened: {trade.id}")
        
        # 5. Set alerts for next session
        self.tg.create_market_alert(
            symbol=symbol,
            condition={"type": "price_level", "level": context.daily.resistance},
            notification_method="email"
        )
    
    def _calculate_position_size(self, account):
        # Risk management: 2% of account per trade
        return (account.equity * 0.02) / 100  # Simplified
    
    def monitor_positions(self):
        """Check all open positions"""
        positions = self.tg.get_positions(self.account_id)
        for pos in positions:
            pnl_percent = (pos.current_price - pos.entry_price) / pos.entry_price * 100
            print(f"{pos.symbol}: {pnl_percent:.2f}% PnL")

# Usage
agent = MarketAgent(
    api_key="cg_pk_live_xxx",
    account_id="acct_123"
)
agent.analyze_and_trade("EURUSD")
agent.monitor_positions()
```

---

## Data Models

### MarketSnapshot
```python
@dataclass
class MarketSnapshot:
    symbol: str
    price: float
    bid: float
    ask: float
    spread: float
    daily_open: float
    daily_high: float
    daily_low: float
    prev_close: float
    change_percent: float
    volume: int
    relative_volume: float
    volatility: float
    session: str  # "US", "EU", "Asia"
    timestamp: datetime
    venue: str
```

### MarketContext
```python
@dataclass
class TimeframeContext:
    trend: str  # "bullish", "bearish", "neutral"
    structure: str
    momentum: str
    volatility: str
    price_location: str

@dataclass
class MarketContext:
    symbol: str
    m5: TimeframeContext
    m15: TimeframeContext
    h1: TimeframeContext
    h4: TimeframeContext
    daily: TimeframeContext
    events: List[MarketEvent]
    cross_market: CrossMarketAnalysis
```

### TradingAccount
```python
@dataclass
class TradingAccount:
    id: str
    broker: str  # "Exness", "cTrader Broker"
    platform: str  # "MT5", "cTrader"
    currency: str
    status: str  # "connected"
    connected_at: datetime
    permissions: List[str]
```

### Position
```python
@dataclass
class Position:
    id: str
    symbol: str
    side: str  # "BUY", "SELL"
    volume: float
    entry_price: float
    current_price: float
    pnl: float
    pnl_percent: float
    opened_at: datetime
    stop_loss: float
    take_profit: float
```

---

## Configuration

### Environment Variables

```bash
# .env
CHARTGAZE_API_KEY=cg_pk_live_xxx
CHARTGAZE_ENV=production  # or development
CHARTGAZE_TIMEOUT=30  # seconds
CHARTGAZE_RETRY_ATTEMPTS=3
```

### Programmatic Configuration

```python
from chartgaze import ChartGaze, Config

config = Config(
    api_key="cg_pk_live_xxx",
    env="production",
    timeout=30,
    retry_attempts=3,
    log_level="DEBUG"
)

tg = ChartGaze(config=config)
```

---

## Logging

```python
import logging
from chartgaze import ChartGaze

logging.basicConfig(level=logging.DEBUG)
tg = ChartGaze(api_key="cg_pk_live_xxx")

# All SDK calls now logged
tg.get_market_snapshot("EURUSD")  # Logs: GET /market/snapshot?symbol=EURUSD
```

---

## Rate Limiting & Pagination

### Respecting Rate Limits

```python
from chartgaze.rate_limit import RateLimitHandler

tg = ChartGaze(api_key="cg_pk_live_xxx")

# SDK automatically handles rate limits
# If limit hit, waits and retries (configurable)

# Check remaining quota
status = tg.get_usage_status()
print(f"Calls remaining this month: {status.remaining}")
```

---

## Testing

```python
import unittest
from chartgaze.mock import MockChartGaze

class TestMyAgent(unittest.TestCase):
    def setUp(self):
        # Use mock client for testing
        self.tg = MockChartGaze()
    
    def test_market_snapshot(self):
        snapshot = self.tg.get_market_snapshot("EURUSD")
        self.assertEqual(snapshot.symbol, "EURUSD")
        self.assertGreater(snapshot.price, 0)

if __name__ == "__main__":
    unittest.main()
```

---

## Contributing

ChartGaze Python SDK is open-source. Contributions welcome:

```bash
# Fork & clone
git clone https://github.com/YOUR_USERNAME/python-sdk.git
cd python-sdk

# Create branch
git checkout -b feature/my-feature

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Submit PR
git push origin feature/my-feature
```

---

## Troubleshooting

### "API key not found"
```python
# Ensure key is in environment or passed explicitly
import os
api_key = os.getenv("CHARTGAZE_API_KEY")
if not api_key:
    raise ValueError("Set CHARTGAZE_API_KEY environment variable")
tg = ChartGaze(api_key=api_key)
```

### "Rate limit exceeded"
```python
# SDK retries automatically, but you can customize
from chartgaze import Config
config = Config(api_key="...", retry_attempts=5)
tg = ChartGaze(config=config)
```

### "Permission denied for trading.execute"
```python
# Ensure you have trading.execute scope enabled in your account dashboard
# Or use propose_trade() for approval workflow
```

---

## API Reference

Full reference: https://docs.chartgaze.dev/python

---

## Support

- **Docs**: https://docs.chartgaze.dev
- **GitHub Issues**: https://github.com/TrainFlow-AI/python-sdk/issues
- **Email**: dev@chartgaze.dev
- **Discord**: [Join our dev community]

---

**SDK Version**: 0.1  
**Last Updated**: 2026-09-29  
**License**: MIT

### TrainFlow AI
- **ChartGaze**: https://chartgaze.live
- **TrainFlow (autonomous trading)**: https://www.trainflow.dev
- **Org**: https://github.com/TrainFlow-AI
