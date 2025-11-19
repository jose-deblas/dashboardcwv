"""URL Repository interface."""
from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.url_entity import URLEntity


class URLRepository(ABC):
    """Abstract repository for URL operations."""

    @abstractmethod
    def get_all(self) -> List[URLEntity]:
        """
        Retrieve all URLs from the repository.

        Returns:
            List of URLEntity objects

        Raises:
            RepositoryException: If retrieval fails
        """
        pass

    @abstractmethod
    def get_by_id(self, url_id: int) -> URLEntity:
        """
        Retrieve a URL by its ID.

        Args:
            url_id: The unique identifier of the URL

        Returns:
            URLEntity object

        Raises:
            RepositoryException: If URL not found or retrieval fails
        """
        pass

    @abstractmethod
    def add(self, url: URLEntity) -> int:
        """
        Add a new URL to the repository.

        Args:
            url: The URLEntity to add

        Returns:
            The ID of the newly created URL

        Raises:
            RepositoryException: If insertion fails
        """
        pass
