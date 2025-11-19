"""MySQL implementation of Core Web Vitals Repository."""
from datetime import date
from typing import List
from mysql.connector import Error, IntegrityError

from src.domain.entities.core_web_vitals import CoreWebVitals
from src.domain.repositories.core_web_vitals_repository import CoreWebVitalsRepository
from src.domain.exceptions import RepositoryException, DuplicateRecordException
from src.infrastructure.database.connection import DatabaseConnection


class MySQLCoreWebVitalsRepository(CoreWebVitalsRepository):
    """MySQL implementation of the Core Web Vitals repository."""

    def __init__(self, db_connection: DatabaseConnection) -> None:
        """
        Initialize repository with database connection.

        Args:
            db_connection: Database connection manager
        """
        self._db = db_connection

    def add(self, metrics: CoreWebVitals) -> None:
        """
        Add Core Web Vitals metrics to the database.

        Args:
            metrics: The CoreWebVitals entity to add

        Raises:
            DuplicateRecordException: If metrics already exist for url_id and execution_date
            RepositoryException: If insertion fails
        """
        try:
            connection = self._db.get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO url_core_web_vitals (
                    url_id, execution_date, performance_score,
                    first_contentful_paint, largest_contentful_paint,
                    total_blocking_time, cumulative_layout_shift,
                    speed_index, time_to_first_byte, time_to_interactive,
                    crux_largest_contentful_paint, crux_interaction_to_next_paint,
                    crux_cumulative_layout_shift, crux_first_contentful_paint,
                    crux_time_to_first_byte
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    metrics.url_id,
                    metrics.execution_date,
                    metrics.performance_score,
                    metrics.first_contentful_paint,
                    metrics.largest_contentful_paint,
                    metrics.total_blocking_time,
                    metrics.cumulative_layout_shift,
                    metrics.speed_index,
                    metrics.time_to_first_byte,
                    metrics.time_to_interactive,
                    metrics.crux_largest_contentful_paint,
                    metrics.crux_interaction_to_next_paint,
                    metrics.crux_cumulative_layout_shift,
                    metrics.crux_first_contentful_paint,
                    metrics.crux_time_to_first_byte,
                ),
            )
            connection.commit()
            cursor.close()

        except IntegrityError as e:
            if 'unique_url_execution' in str(e).lower() or 'duplicate' in str(e).lower():
                raise DuplicateRecordException(
                    f"Metrics already exist for url_id={metrics.url_id} "
                    f"on date={metrics.execution_date}"
                ) from e
            raise RepositoryException(f"Failed to add metrics: {e}") from e
        except Error as e:
            raise RepositoryException(f"Failed to add metrics: {e}") from e

    def exists(self, url_id: int, execution_date: date) -> bool:
        """
        Check if metrics exist for a given URL and date.

        Args:
            url_id: The URL identifier
            execution_date: The date to check

        Returns:
            True if metrics exist, False otherwise

        Raises:
            RepositoryException: If check fails
        """
        try:
            connection = self._db.get_connection()
            cursor = connection.cursor()

            query = """
                SELECT COUNT(*) as count
                FROM url_core_web_vitals
                WHERE url_id = %s AND execution_date = %s
            """
            cursor.execute(query, (url_id, execution_date))
            result = cursor.fetchone()
            cursor.close()

            return result[0] > 0 if result else False

        except Error as e:
            raise RepositoryException(
                f"Failed to check if metrics exist: {e}"
            ) from e

    def get_by_url_and_date(self, url_id: int, execution_date: date) -> CoreWebVitals:
        """
        Retrieve metrics for a specific URL and date.

        Args:
            url_id: The URL identifier
            execution_date: The date to retrieve

        Returns:
            CoreWebVitals entity

        Raises:
            RepositoryException: If metrics not found or retrieval fails
        """
        try:
            connection = self._db.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT *
                FROM url_core_web_vitals
                WHERE url_id = %s AND execution_date = %s
            """
            cursor.execute(query, (url_id, execution_date))
            row = cursor.fetchone()
            cursor.close()

            if not row:
                raise RepositoryException(
                    f"Metrics not found for url_id={url_id}, date={execution_date}"
                )

            return CoreWebVitals(
                url_id=row['url_id'],
                execution_date=row['execution_date'],
                performance_score=row['performance_score'],
                first_contentful_paint=row['first_contentful_paint'],
                largest_contentful_paint=row['largest_contentful_paint'],
                total_blocking_time=row['total_blocking_time'],
                cumulative_layout_shift=row['cumulative_layout_shift'],
                speed_index=row['speed_index'],
                time_to_first_byte=row['time_to_first_byte'],
                time_to_interactive=row['time_to_interactive'],
                crux_largest_contentful_paint=row['crux_largest_contentful_paint'],
                crux_interaction_to_next_paint=row['crux_interaction_to_next_paint'],
                crux_cumulative_layout_shift=row['crux_cumulative_layout_shift'],
                crux_first_contentful_paint=row['crux_first_contentful_paint'],
                crux_time_to_first_byte=row['crux_time_to_first_byte'],
            )

        except Error as e:
            raise RepositoryException(f"Failed to retrieve metrics: {e}") from e

    def get_urls_without_data_for_date(self, execution_date: date) -> List[int]:
        """
        Get list of URL IDs that don't have metrics for the specified date.

        Args:
            execution_date: The date to check

        Returns:
            List of URL IDs without metrics for the date

        Raises:
            RepositoryException: If query fails
        """
        try:
            connection = self._db.get_connection()
            cursor = connection.cursor()

            query = """
                SELECT u.url_id
                FROM urls u
                LEFT JOIN url_core_web_vitals cwv
                    ON u.url_id = cwv.url_id
                    AND cwv.execution_date = %s
                WHERE cwv.id IS NULL
                ORDER BY u.url_id
            """
            cursor.execute(query, (execution_date,))
            rows = cursor.fetchall()
            cursor.close()

            return [row[0] for row in rows]

        except Error as e:
            raise RepositoryException(
                f"Failed to get URLs without data: {e}"
            ) from e
