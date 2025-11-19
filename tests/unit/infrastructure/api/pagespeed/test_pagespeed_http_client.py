"""Tests for PageSpeed HTTP client."""
import pytest
from unittest.mock import Mock, patch
from requests.exceptions import HTTPError, Timeout, RequestException

from src.infrastructure.api.pagespeed.auth.pagespeed_auth_provider import (
    PageSpeedAuthProvider,
)
from src.infrastructure.api.pagespeed.http.pagespeed_http_client import (
    PageSpeedHTTPClient,
)


class TestPageSpeedHTTPClient:
    """Test suite for PageSpeedHTTPClient."""

    @pytest.fixture
    def auth_provider(self):
        """Create mock auth provider."""
        provider = Mock(spec=PageSpeedAuthProvider)
        provider.get_api_key.return_value = "test_api_key"
        return provider

    @pytest.fixture
    def http_client(self, auth_provider):
        """Create HTTP client for testing."""
        return PageSpeedHTTPClient(
            auth_provider=auth_provider,
            max_retries=2,
            initial_backoff=0.1,
            backoff_multiplier=2.0,
            timeout=30
        )

    @patch('src.infrastructure.api.pagespeed.http.pagespeed_http_client.requests.get')
    def test_fetch_metrics_success(self, mock_get, http_client, sample_pagespeed_response):
        """Test successful API call."""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = sample_pagespeed_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Act
        result = http_client.fetch_metrics(
            url="https://example.com",
            strategy="mobile",
            categories=["performance"]
        )

        # Assert
        assert result == sample_pagespeed_response
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]['params']['url'] == "https://example.com"
        assert call_args[1]['params']['strategy'] == "mobile"
        assert call_args[1]['params']['key'] == "test_api_key"

    @patch('src.infrastructure.api.pagespeed.http.pagespeed_http_client.requests.get')
    @patch('src.infrastructure.api.pagespeed.http.pagespeed_http_client.time.sleep')
    def test_fetch_metrics_retry_on_500(
        self, mock_sleep, mock_get, http_client, sample_pagespeed_response
    ):
        """Test retry logic on 500 error."""
        # Arrange
        mock_error_response = Mock()
        mock_error_response.status_code = 500
        error = HTTPError(response=mock_error_response)

        mock_success_response = Mock()
        mock_success_response.json.return_value = sample_pagespeed_response
        mock_success_response.raise_for_status = Mock()

        # First call fails, second succeeds
        mock_get.side_effect = [
            Mock(raise_for_status=Mock(side_effect=error)),
            mock_success_response
        ]

        # Act
        result = http_client.fetch_metrics(
            url="https://example.com",
            strategy="mobile",
            categories=["performance"]
        )

        # Assert
        assert result == sample_pagespeed_response
        assert mock_get.call_count == 2
        mock_sleep.assert_called_once()

    @patch('src.infrastructure.api.pagespeed.http.pagespeed_http_client.requests.get')
    def test_fetch_metrics_no_retry_on_404(self, mock_get, http_client):
        """Test no retry on 404 client error."""
        # Arrange
        mock_error_response = Mock()
        mock_error_response.status_code = 404
        error = HTTPError(response=mock_error_response)
        mock_get.return_value.raise_for_status.side_effect = error

        # Act & Assert
        with pytest.raises(HTTPError):
            http_client.fetch_metrics(
                url="https://example.com",
                strategy="mobile",
                categories=["performance"]
            )

        # Should only be called once (no retry)
        assert mock_get.call_count == 1

    @patch('src.infrastructure.api.pagespeed.http.pagespeed_http_client.requests.get')
    @patch('src.infrastructure.api.pagespeed.http.pagespeed_http_client.time.sleep')
    def test_fetch_metrics_retry_on_429(
        self, mock_sleep, mock_get, http_client, sample_pagespeed_response
    ):
        """Test retry on 429 rate limit error."""
        # Arrange
        mock_error_response = Mock()
        mock_error_response.status_code = 429
        error = HTTPError(response=mock_error_response)

        mock_success_response = Mock()
        mock_success_response.json.return_value = sample_pagespeed_response
        mock_success_response.raise_for_status = Mock()

        # First call fails with 429, second succeeds
        mock_get.side_effect = [
            Mock(raise_for_status=Mock(side_effect=error)),
            mock_success_response
        ]

        # Act
        result = http_client.fetch_metrics(
            url="https://example.com",
            strategy="mobile",
            categories=["performance"]
        )

        # Assert
        assert result == sample_pagespeed_response
        assert mock_get.call_count == 2

    @patch('src.infrastructure.api.pagespeed.http.pagespeed_http_client.requests.get')
    @patch('src.infrastructure.api.pagespeed.http.pagespeed_http_client.time.sleep')
    def test_fetch_metrics_exhaust_retries(self, mock_sleep, mock_get, http_client):
        """Test failure after exhausting all retries."""
        # Arrange
        mock_get.side_effect = Timeout("Connection timeout")

        # Act & Assert
        with pytest.raises(Timeout):
            http_client.fetch_metrics(
                url="https://example.com",
                strategy="mobile",
                categories=["performance"]
            )

        # Should retry max_retries + 1 times (initial + 2 retries = 3 total)
        assert mock_get.call_count == 3
