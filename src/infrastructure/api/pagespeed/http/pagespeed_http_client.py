"""HTTP client for PageSpeed Insights API with retry logic."""
import time
import logging
from typing import Dict, Any, List
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

from src.infrastructure.api.pagespeed.auth.pagespeed_auth_provider import (
    PageSpeedAuthProvider,
)


logger = logging.getLogger(__name__)


class PageSpeedHTTPClient:
    """HTTP client for PageSpeed Insights API with exponential backoff retry."""

    BASE_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def __init__(
        self,
        auth_provider: PageSpeedAuthProvider,
        max_retries: int = 3,
        initial_backoff: float = 1.0,
        backoff_multiplier: float = 2.0,
        timeout: int = 60,
    ) -> None:
        """
        Initialize HTTP client with retry configuration.

        Args:
            auth_provider: Authentication provider for API key
            max_retries: Maximum number of retry attempts
            initial_backoff: Initial backoff delay in seconds
            backoff_multiplier: Multiplier for exponential backoff
            timeout: Request timeout in seconds
        """
        self._auth = auth_provider
        self._max_retries = max_retries
        self._initial_backoff = initial_backoff
        self._backoff_multiplier = backoff_multiplier
        self._timeout = timeout

    def fetch_metrics(
        self, url: str, strategy: str, categories: List[str]
    ) -> Dict[str, Any]:
        """
        Fetch PageSpeed metrics for a URL with retry logic.

        Args:
            url: URL to analyze
            strategy: Device strategy ('mobile' or 'desktop')
            categories: List of categories to analyze (e.g., ['performance'])

        Returns:
            JSON response from PageSpeed Insights API

        Raises:
            HTTPError: If request fails after all retries
            RequestException: If request encounters an error
        """
        params = {
            'url': url,
            'key': self._auth.get_api_key(),
            'strategy': strategy,
            'category': categories,
        }

        last_exception = None
        backoff = self._initial_backoff

        for attempt in range(self._max_retries + 1):
            try:
                logger.info(
                    f"Fetching PageSpeed data for {url} "
                    f"(strategy={strategy}, attempt={attempt + 1})"
                )

                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    timeout=self._timeout
                )

                response.raise_for_status()
                logger.info(f"Successfully fetched data for {url}")
                return response.json()

            except HTTPError as e:
                status_code = e.response.status_code if e.response else None
                logger.warning(
                    f"HTTP error {status_code} for {url} on attempt {attempt + 1}: {e}"
                )

                # Don't retry on client errors (4xx) except 429 (rate limit)
                if status_code and 400 <= status_code < 500 and status_code != 429:
                    logger.error(f"Client error {status_code}, not retrying")
                    raise

                last_exception = e

            except Timeout as e:
                logger.warning(f"Timeout for {url} on attempt {attempt + 1}: {e}")
                last_exception = e

            except RequestException as e:
                logger.warning(f"Request error for {url} on attempt {attempt + 1}: {e}")
                last_exception = e

            # If not the last attempt, wait before retrying
            if attempt < self._max_retries:
                wait_time = backoff * (self._backoff_multiplier ** attempt)
                logger.info(f"Waiting {wait_time:.2f}s before retry...")
                time.sleep(wait_time)
            else:
                logger.error(
                    f"Failed to fetch data for {url} after {self._max_retries + 1} attempts"
                )

        # If we exhausted all retries, raise the last exception
        if last_exception:
            raise last_exception

        # This should never happen, but just in case
        raise RequestException(f"Failed to fetch data for {url}")
