"""Authentication provider for PageSpeed Insights API."""
import os
from typing import Optional


class PageSpeedAuthProvider:
    """Manages API key authentication for PageSpeed Insights API."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialize auth provider.

        Args:
            api_key: PageSpeed Insights API key (defaults to env var)
        """
        self._api_key = api_key or os.getenv('PAGESPEED_INSIGHTS_API_KEY')

    def get_api_key(self) -> str:
        """
        Get the API key for authentication.

        Returns:
            API key string

        Raises:
            ValueError: If API key is not configured
        """
        if not self._api_key or self._api_key == 'your_api_key_here':
            raise ValueError(
                "PAGESPEED_INSIGHTS_API_KEY not configured. "
                "Get your API key from: "
                "https://developers.google.com/speed/docs/insights/v5/get-started"
            )
        return self._api_key

    def is_configured(self) -> bool:
        """
        Check if API key is properly configured.

        Returns:
            True if API key is configured, False otherwise
        """
        return bool(self._api_key and self._api_key != 'your_api_key_here')
