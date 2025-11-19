"""Tests for URLEntity."""
import pytest

from src.domain.entities.url_entity import URLEntity
from src.domain.exceptions import InvalidURLException, InvalidDeviceException


class TestURLEntity:
    """Test suite for URLEntity validation."""

    def test_create_valid_url_entity(self):
        """Test creating a valid URL entity."""
        # Act
        entity = URLEntity(
            url_id=1,
            url="https://example.com",
            device="mobile",
            page_type="home",
            brand="example",
            category="test",
            country_id="US",
        )

        # Assert
        assert entity.url_id == 1
        assert entity.url == "https://example.com"
        assert entity.device == "mobile"

    def test_invalid_empty_url(self):
        """Test that empty URL raises InvalidURLException."""
        # Act & Assert
        with pytest.raises(InvalidURLException, match="URL cannot be empty"):
            URLEntity(
                url_id=1,
                url="",
                device="mobile",
                page_type="home",
                brand="example",
                category="test",
                country_id="US",
            )

    def test_invalid_device_type(self):
        """Test that invalid device type raises InvalidDeviceException."""
        # Act & Assert
        with pytest.raises(InvalidDeviceException, match="must be 'mobile' or 'desktop'"):
            URLEntity(
                url_id=1,
                url="https://example.com",
                device="tablet",
                page_type="home",
                brand="example",
                category="test",
                country_id="US",
            )

    def test_invalid_url_without_protocol(self):
        """Test that URL without protocol raises InvalidURLException."""
        # Act & Assert
        with pytest.raises(InvalidURLException, match="must start with http"):
            URLEntity(
                url_id=1,
                url="example.com",
                device="mobile",
                page_type="home",
                brand="example",
                category="test",
                country_id="US",
            )

    def test_desktop_device_is_valid(self):
        """Test that desktop device type is valid."""
        # Act
        entity = URLEntity(
            url_id=1,
            url="https://example.com",
            device="desktop",
            page_type="home",
            brand="example",
            category="test",
            country_id="US",
        )

        # Assert
        assert entity.device == "desktop"
