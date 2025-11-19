"""Use case for collecting PageSpeed Insights data."""
from datetime import date
import logging
from typing import List

from src.domain.repositories.url_repository import URLRepository
from src.domain.repositories.core_web_vitals_repository import CoreWebVitalsRepository
from src.domain.entities.url_entity import URLEntity
from src.domain.exceptions import RepositoryException, DuplicateRecordException
from src.infrastructure.api.pagespeed.pagespeed_client_facade import (
    PageSpeedClientFacade,
)
from src.application.dto.execution_summary import ExecutionSummary


logger = logging.getLogger(__name__)


class CollectPageSpeedDataUseCase:
    """
    Use case for collecting Core Web Vitals data from PageSpeed Insights API.

    This use case orchestrates the process of:
    1. Fetching URLs that need data collection
    2. Calling PageSpeed Insights API for each URL
    3. Storing the results in the database
    4. Handling errors gracefully and continuing with remaining URLs
    """

    def __init__(
        self,
        url_repository: URLRepository,
        cwv_repository: CoreWebVitalsRepository,
        pagespeed_client: PageSpeedClientFacade,
    ) -> None:
        """
        Initialize use case with dependencies.

        Args:
            url_repository: Repository for URL operations
            cwv_repository: Repository for Core Web Vitals operations
            pagespeed_client: Client for PageSpeed Insights API
        """
        self._url_repo = url_repository
        self._cwv_repo = cwv_repository
        self._pagespeed_client = pagespeed_client

    def execute(self, execution_date: date) -> ExecutionSummary:
        """
        Execute the data collection process.

        Args:
            execution_date: Date for which to collect data

        Returns:
            ExecutionSummary with results of the operation
        """
        logger.info(f"Starting data collection for date: {execution_date}")

        # Get all URLs from database
        all_urls = self._get_all_urls()
        logger.info(f"Found {len(all_urls)} total URLs in database")

        # Initialize summary
        summary = ExecutionSummary(
            execution_date=execution_date,
            total_urls=len(all_urls)
        )

        if len(all_urls) == 0:
            logger.warning("No URLs found in database")
            return summary

        # Process each URL
        for url_entity in all_urls:
            self._process_url(url_entity, execution_date, summary)

        # Log final summary
        logger.info(
            f"Data collection completed: "
            f"Total={summary.total_urls}, "
            f"Successful={summary.successful}, "
            f"Failed={summary.failed}, "
            f"Skipped={summary.skipped}"
        )

        return summary

    def _get_all_urls(self) -> List[URLEntity]:
        """
        Fetch all URLs from repository.

        Returns:
            List of URL entities

        Raises:
            RepositoryException: If fetching URLs fails
        """
        try:
            return self._url_repo.get_all()
        except RepositoryException as e:
            logger.error(f"Failed to fetch URLs from database: {e}")
            raise

    def _process_url(
        self,
        url_entity: URLEntity,
        execution_date: date,
        summary: ExecutionSummary
    ) -> None:
        """
        Process a single URL: check if data exists, fetch if needed, store results.

        Args:
            url_entity: URL entity to process
            execution_date: Execution date
            summary: Execution summary to update
        """
        url_id = url_entity.url_id
        url = url_entity.url

        try:
            # Check if data already exists for this URL and date
            if self._cwv_repo.exists(url_id, execution_date):
                logger.info(
                    f"Skipping URL {url_id} ({url}): data already exists for {execution_date}"
                )
                summary.add_skipped(url_id, url)
                return

            # Fetch data from PageSpeed Insights API
            logger.info(f"Processing URL {url_id}: {url} ({url_entity.device})")
            core_web_vitals = self._pagespeed_client.fetch_core_web_vitals(
                url_id=url_id,
                url=url,
                device=url_entity.device,
                execution_date=execution_date
            )

            # Store in database
            self._cwv_repo.add(core_web_vitals)
            logger.info(
                f"Successfully stored metrics for URL {url_id}: "
                f"Performance Score = {core_web_vitals.performance_score}"
            )
            summary.add_success(url_id, url)

        except DuplicateRecordException as e:
            # This shouldn't happen due to the exists check, but handle it anyway
            logger.warning(f"Duplicate record for URL {url_id} ({url}): {e}")
            summary.add_skipped(url_id, url)

        except Exception as e:
            # Log error and continue with next URL
            error_msg = f"{type(e).__name__}: {str(e)}"
            logger.error(f"Failed to process URL {url_id} ({url}): {error_msg}")
            summary.add_failure(url_id, url, error_msg)
