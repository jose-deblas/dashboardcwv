"""MySQL implementation of URL Repository."""
from typing import List
from mysql.connector import Error

from src.domain.entities.url_entity import URLEntity
from src.domain.repositories.url_repository import URLRepository
from src.domain.exceptions import RepositoryException
from src.infrastructure.database.connection import DatabaseConnection


class MySQLURLRepository(URLRepository):
    """MySQL implementation of the URL repository."""

    def __init__(self, db_connection: DatabaseConnection) -> None:
        """
        Initialize repository with database connection.

        Args:
            db_connection: Database connection manager
        """
        self._db = db_connection

    def get_all(self) -> List[URLEntity]:
        """
        Retrieve all URLs from the database.

        Returns:
            List of URLEntity objects

        Raises:
            RepositoryException: If retrieval fails
        """
        try:
            connection = self._db.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT url_id, url, device, page_type, brand, category, country_id, created_at
                FROM urls
                ORDER BY url_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            return [
                URLEntity(
                    url_id=row['url_id'],
                    url=row['url'],
                    device=row['device'],
                    page_type=row['page_type'],
                    brand=row['brand'],
                    category=row['category'],
                    country_id=row['country_id'],
                    created_at=row['created_at'],
                )
                for row in rows
            ]
        except Error as e:
            raise RepositoryException(f"Failed to retrieve URLs: {e}") from e

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
        try:
            connection = self._db.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT url_id, url, device, page_type, brand, category, country_id, created_at
                FROM urls
                WHERE url_id = %s
            """
            cursor.execute(query, (url_id,))
            row = cursor.fetchone()
            cursor.close()

            if not row:
                raise RepositoryException(f"URL with ID {url_id} not found")

            return URLEntity(
                url_id=row['url_id'],
                url=row['url'],
                device=row['device'],
                page_type=row['page_type'],
                brand=row['brand'],
                category=row['category'],
                country_id=row['country_id'],
                created_at=row['created_at'],
            )
        except Error as e:
            raise RepositoryException(f"Failed to retrieve URL: {e}") from e

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
        try:
            connection = self._db.get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO urls (url, device, page_type, brand, category, country_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    url.url,
                    url.device,
                    url.page_type,
                    url.brand,
                    url.category,
                    url.country_id,
                ),
            )
            connection.commit()

            url_id = cursor.lastrowid
            cursor.close()

            return url_id
        except Error as e:
            raise RepositoryException(f"Failed to add URL: {e}") from e
