"""Facade for PageSpeed Insights API client."""
from datetime import date
import logging

from src.domain.entities.core_web_vitals import CoreWebVitals
from src.infrastructure.api.pagespeed.auth.pagespeed_auth_provider import (
    PageSpeedAuthProvider,
)
from src.infrastructure.api.pagespeed.http.pagespeed_http_client import (
    PageSpeedHTTPClient,
)
from src.infrastructure.api.pagespeed.dto.pagespeed_response import (
    PageSpeedInsightsResponse,
)
from src.infrastructure.api.pagespeed.mappers.pagespeed_mapper import PageSpeedMapper


logger = logging.getLogger(__name__)


class PageSpeedClientFacade:
    """
    Facade providing a clean API for PageSpeed Insights operations.

    Combines authentication, HTTP client, and mapping functionality.
    """

    def __init__(
        self,
        auth_provider: PageSpeedAuthProvider,
        http_client: PageSpeedHTTPClient,
        mapper: PageSpeedMapper,
    ) -> None:
        """
        Initialize facade with dependencies.

        Args:
            auth_provider: Authentication provider
            http_client: HTTP client for API calls
            mapper: Mapper for converting responses to domain entities
        """
        self._auth = auth_provider
        self._http_client = http_client
        self._mapper = mapper

    def fetch_core_web_vitals(
        self,
        url_id: int,
        url: str,
        device: str,
        execution_date: date,
    ) -> CoreWebVitals:
        """
        Fetch Core Web Vitals for a URL.

        Args:
            url_id: URL identifier
            url: URL to analyze
            device: Device type ('mobile' or 'desktop')
            execution_date: Execution date for the metrics

        Returns:
            CoreWebVitals domain entity

        Raises:
            ValueError: If API key is not configured
            HTTPError: If API request fails
            RequestException: If request encounters an error
        """
        logger.info(f"Fetching Core Web Vitals for URL {url_id}: {url} ({device})")

        # Fetch data from API
        response_json = self._http_client.fetch_metrics(
            url=url,
            strategy=device,
            categories=['performance']
        )

        # Parse response as DTO
        response_dto = PageSpeedInsightsResponse(response_json)

        # Map to domain entity
        core_web_vitals = self._mapper.to_core_web_vitals(
            url_id=url_id,
            execution_date=execution_date,
            response=response_dto
        )

        logger.info(
            f"Successfully fetched metrics for URL {url_id}: "
            f"Performance Score = {core_web_vitals.performance_score}"
        )

        return core_web_vitals
