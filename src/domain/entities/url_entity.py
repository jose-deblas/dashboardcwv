"""URL Entity representing a monitored URL in the system."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.exceptions import InvalidURLException, InvalidDeviceException


@dataclass(frozen=True)
class URLEntity:
    """
    Entity representing a URL to be monitored for Core Web Vitals.

    Attributes:
        url_id: Unique identifier for the URL
        url: The actual URL string
        device: Device type (mobile or desktop)
        page_type: Type of page being monitored
        brand: Brand associated with the URL
        category: Category classification
        country_id: Country identifier
        created_at: Timestamp when the URL was created
    """
    url_id: int
    url: str
    device: str
    page_type: str
    brand: str
    category: str
    country_id: str
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate entity after initialization."""
        if not self.url or not self.url.strip():
            raise InvalidURLException("URL cannot be empty")

        if self.device not in ('mobile', 'desktop'):
            raise InvalidDeviceException(
                f"Device must be 'mobile' or 'desktop', got: {self.device}"
            )

        if not self.url.startswith(('http://', 'https://')):
            raise InvalidURLException(
                f"URL must start with http:// or https://, got: {self.url}"
            )
