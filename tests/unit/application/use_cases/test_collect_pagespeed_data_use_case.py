"""Tests for CollectPageSpeedDataUseCase."""
import pytest
from unittest.mock import Mock
from datetime import date

from src.application.use_cases.collect_pagespeed_data_use_case import (
    CollectPageSpeedDataUseCase,
)
from src.domain.entities.url_entity import URLEntity
from src.domain.entities.core_web_vitals import CoreWebVitals
from src.domain.exceptions import RepositoryException, DuplicateRecordException


class TestCollectPageSpeedDataUseCase:
    """Test suite for CollectPageSpeedDataUseCase."""

    @pytest.fixture
    def url_repository(self):
        """Create mock URL repository."""
        return Mock()

    @pytest.fixture
    def cwv_repository(self):
        """Create mock Core Web Vitals repository."""
        return Mock()

    @pytest.fixture
    def pagespeed_client(self):
        """Create mock PageSpeed client."""
        return Mock()

    @pytest.fixture
    def use_case(self, url_repository, cwv_repository, pagespeed_client):
        """Create use case instance with mocked dependencies."""
        return CollectPageSpeedDataUseCase(
            url_repository=url_repository,
            cwv_repository=cwv_repository,
            pagespeed_client=pagespeed_client,
        )

    @pytest.fixture
    def sample_urls(self):
        """Create sample URL entities."""
        return [
            URLEntity(
                url_id=1,
                url="https://example.com",
                device="mobile",
                page_type="home",
                brand="example",
                category="test",
                country_id="US",
            ),
            URLEntity(
                url_id=2,
                url="https://example.org",
                device="desktop",
                page_type="product",
                brand="example",
                category="test",
                country_id="UK",
            ),
        ]

    @pytest.fixture
    def sample_cwv(self):
        """Create sample Core Web Vitals entity."""
        return CoreWebVitals(
            url_id=1,
            execution_date=date(2025, 11, 19),
            performance_score=85.0,
            first_contentful_paint=1234.5,
        )

    def test_execute_with_no_urls(self, use_case, url_repository):
        """Test execution when no URLs exist in database."""
        # Arrange
        url_repository.get_all.return_value = []
        execution_date = date(2025, 11, 19)

        # Act
        summary = use_case.execute(execution_date)

        # Assert
        assert summary.total_urls == 0
        assert summary.successful == 0
        assert summary.failed == 0
        assert summary.skipped == 0

    def test_execute_success(
        self,
        use_case,
        url_repository,
        cwv_repository,
        pagespeed_client,
        sample_urls,
        sample_cwv,
    ):
        """Test successful execution with multiple URLs."""
        # Arrange
        execution_date = date(2025, 11, 19)
        url_repository.get_all.return_value = sample_urls
        cwv_repository.exists.return_value = False
        pagespeed_client.fetch_core_web_vitals.return_value = sample_cwv

        # Act
        summary = use_case.execute(execution_date)

        # Assert
        assert summary.total_urls == 2
        assert summary.successful == 2
        assert summary.failed == 0
        assert summary.skipped == 0
        assert pagespeed_client.fetch_core_web_vitals.call_count == 2
        assert cwv_repository.add.call_count == 2

    def test_execute_skips_existing_data(
        self,
        use_case,
        url_repository,
        cwv_repository,
        pagespeed_client,
        sample_urls,
    ):
        """Test that URLs with existing data are skipped."""
        # Arrange
        execution_date = date(2025, 11, 19)
        url_repository.get_all.return_value = sample_urls
        cwv_repository.exists.side_effect = [True, False]  # First exists, second doesn't
        pagespeed_client.fetch_core_web_vitals.return_value = CoreWebVitals(
            url_id=2, execution_date=execution_date, performance_score=75.0
        )

        # Act
        summary = use_case.execute(execution_date)

        # Assert
        assert summary.total_urls == 2
        assert summary.successful == 1
        assert summary.failed == 0
        assert summary.skipped == 1
        # Should only fetch for the second URL
        assert pagespeed_client.fetch_core_web_vitals.call_count == 1
        assert cwv_repository.add.call_count == 1

    def test_execute_continues_on_api_error(
        self,
        use_case,
        url_repository,
        cwv_repository,
        pagespeed_client,
        sample_urls,
        sample_cwv,
    ):
        """Test that execution continues when API call fails for one URL."""
        # Arrange
        execution_date = date(2025, 11, 19)
        url_repository.get_all.return_value = sample_urls
        cwv_repository.exists.return_value = False
        # First call fails, second succeeds
        pagespeed_client.fetch_core_web_vitals.side_effect = [
            Exception("API Error"),
            sample_cwv,
        ]

        # Act
        summary = use_case.execute(execution_date)

        # Assert
        assert summary.total_urls == 2
        assert summary.successful == 1
        assert summary.failed == 1
        assert summary.skipped == 0
        # Verify error details
        failed_urls = summary.get_failed_urls()
        assert len(failed_urls) == 1
        assert failed_urls[0].url_id == 1
        assert "API Error" in failed_urls[0].error_message

    def test_execute_handles_duplicate_record_exception(
        self,
        use_case,
        url_repository,
        cwv_repository,
        pagespeed_client,
        sample_urls,
        sample_cwv,
    ):
        """Test handling of DuplicateRecordException."""
        # Arrange
        execution_date = date(2025, 11, 19)
        url_repository.get_all.return_value = [sample_urls[0]]
        cwv_repository.exists.return_value = False
        pagespeed_client.fetch_core_web_vitals.return_value = sample_cwv
        cwv_repository.add.side_effect = DuplicateRecordException("Duplicate")

        # Act
        summary = use_case.execute(execution_date)

        # Assert
        assert summary.total_urls == 1
        assert summary.successful == 0
        assert summary.failed == 0
        assert summary.skipped == 1

    def test_execute_propagates_repository_exception(
        self,
        use_case,
        url_repository,
    ):
        """Test that RepositoryException is propagated."""
        # Arrange
        execution_date = date(2025, 11, 19)
        url_repository.get_all.side_effect = RepositoryException("DB Error")

        # Act & Assert
        with pytest.raises(RepositoryException):
            use_case.execute(execution_date)
