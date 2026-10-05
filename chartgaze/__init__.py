"""ChartGaze Python SDK — connect agents to market structure, events, and accounts."""

__version__ = "0.1.0"


class ChartGaze:
    """Client for ChartGaze HTTP / MCP-backed market intelligence."""

    def __init__(self, api_key=None, oauth_token=None, base_url: str = "https://api.chartgaze.live"):
        self.api_key = api_key
        self.oauth_token = oauth_token
        self.base_url = base_url.rstrip("/")

    def get_market_snapshot(self, symbol: str):
        raise NotImplementedError("Install the published package and pass a live API key — see README.")

    def get_market_context(self, symbol: str):
        raise NotImplementedError("See README for MCP / REST usage.")


__all__ = ["ChartGaze", "__version__"]
