"""
MySQL implementation of dashboard repository.

This module implements the DashboardRepository interface for MySQL database.
Following Clean Architecture principles with proper dependency injection.
"""

from datetime import date
from typing import Dict, List, Optional, Tuple

from mysql.connector import Error as MySQLError

from src.domain.repositories.brand_repository import BrandRepository
from src.domain.repositories.dashboard_repository import DashboardRepository
from src.infrastructure.database.connection import DatabaseConnection


class MySQLDashboardRepository(DashboardRepository):
    """
    MySQL implementation of dashboard repository.

    This repository handles complex aggregation queries for dashboard visualizations.
    """

    def __init__(
        self, db_connection: DatabaseConnection, brand_repository: BrandRepository
    ):
        """
        Initialize repository with database connection and brand repository.

        Args:
            db_connection: Database connection instance for dependency injection
            brand_repository: Brand repository for accessing target brands
        """
        self._db = db_connection
        self._brand_repository = brand_repository

    def get_date_range(self) -> Tuple[Optional[date], Optional[date]]:
        """Get the minimum and maximum execution dates available in the database."""
        query = """
            SELECT
                MIN(execution_date) as min_date,
                MAX(execution_date) as max_date
            FROM url_core_web_vitals
        """

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

            if result:
                return (result.get("min_date"), result.get("max_date"))
            return (None, None)

        except MySQLError as e:
            raise RuntimeError(f"Failed to get date range: {str(e)}")

    def get_target_brands(self) -> List[str]:
        """Get list of distinct brands available in the database."""
        query = """
            SELECT brand
            FROM url_brands
            WHERE target_brand = TRUE
            ORDER BY brand ASC
        """

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            return [row[0] for row in results if row[0]]

        except MySQLError as e:
            raise RuntimeError(f"Failed to get available brands: {str(e)}")

    def get_available_countries(self) -> List[str]:
        """Get list of distinct countries available in the database."""
        query = """
            SELECT DISTINCT country_id
            FROM urls
            WHERE country_id IS NOT NULL
            ORDER BY country_id ASC
        """

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            return [row[0] for row in results if row[0]]

        except MySQLError as e:
            raise RuntimeError(f"Failed to get available countries: {str(e)}")

    def get_available_page_types(self) -> List[str]:
        """Get list of distinct page types available in the database."""
        query = """
            SELECT DISTINCT page_type
            FROM urls
            WHERE page_type IS NOT NULL
            ORDER BY page_type ASC
        """

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            return [row[0] for row in results if row[0]]

        except MySQLError as e:
            raise RuntimeError(f"Failed to get available page types: {str(e)}")

    def get_performance_metrics_by_date(
        self,
        target_date: date,
        device: str,
        brands: Optional[List[str]] = None,
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
    ) -> Optional[float]:
        """Get average performance score for a specific date with optional filters."""
        query = """
            SELECT AVG(cwv.performance_score) as avg_score
            FROM url_core_web_vitals cwv
            INNER JOIN urls u ON cwv.url_id = u.url_id
            WHERE cwv.execution_date = %s
                AND u.device = %s
                AND cwv.performance_score IS NOT NULL
        """

        params: List = [target_date, device]

        # Add optional filters
        if brands:
            placeholders = ",".join(["%s"] * len(brands))
            query += f" AND u.brand IN ({placeholders})"
            params.extend(brands)

        if countries:
            placeholders = ",".join(["%s"] * len(countries))
            query += f" AND u.country_id IN ({placeholders})"
            params.extend(countries)

        if page_types:
            placeholders = ",".join(["%s"] * len(page_types))
            query += f" AND u.page_type IN ({placeholders})"
            params.extend(page_types)

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()

            if result and result.get("avg_score") is not None:
                return float(result["avg_score"])
            return None

        except MySQLError as e:
            raise RuntimeError(f"Failed to get performance metrics: {str(e)}")

    def get_performance_time_series(
        self,
        start_date: date,
        end_date: date,
        device: str,
        brands: Optional[List[str]] = None,
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Get performance score time series data with optional filters."""
        query = """
            SELECT
                cwv.execution_date,
                AVG(cwv.performance_score) as avg_performance_score
            FROM url_core_web_vitals cwv
            INNER JOIN urls u ON cwv.url_id = u.url_id
            WHERE cwv.execution_date BETWEEN %s AND %s
                AND u.device = %s
                AND cwv.performance_score IS NOT NULL
        """

        params: List = [start_date, end_date, device]

        # Add optional filters
        if brands:
            placeholders = ",".join(["%s"] * len(brands))
            query += f" AND u.brand IN ({placeholders})"
            params.extend(brands)

        if countries:
            placeholders = ",".join(["%s"] * len(countries))
            query += f" AND u.country_id IN ({placeholders})"
            params.extend(countries)

        if page_types:
            placeholders = ",".join(["%s"] * len(page_types))
            query += f" AND u.page_type IN ({placeholders})"
            params.extend(page_types)

        query += """
            GROUP BY cwv.execution_date
            ORDER BY cwv.execution_date ASC
        """

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            return [
                {
                    "execution_date": row["execution_date"],
                    "avg_performance_score": (
                        float(row["avg_performance_score"])
                        if row["avg_performance_score"] is not None
                        else None
                    ),
                }
                for row in results
            ]

        except MySQLError as e:
            raise RuntimeError(f"Failed to get performance time series: {str(e)}")

    def get_brand_rankings(
        self,
        target_date: date,
        device: str,
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
        limit: int = 3,
    ) -> List[Dict]:
        """Get brand rankings by average performance score for a specific date."""
        # First, get top N brands
        query, params = self._build_rankings_query_and_params(
            target_date, device, countries, page_types
        )

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            all_brands = cursor.fetchall()
            cursor.close()

            if not all_brands:
                return []

            # Get top N brands
            top_brands = all_brands[:limit]

            # Check if target brands are in top N
            top_brand_names = {b["brand"] for b in top_brands}
            target_brands = set(self._brand_repository.get_target_brands())
            missing_targets = target_brands - top_brand_names

            # Add missing target brands if they exist in data
            result = list(top_brands)
            for brand_data in all_brands[limit:]:
                if brand_data["brand"] in missing_targets:
                    result.append(brand_data)

            return result

        except MySQLError as e:
            raise RuntimeError(f"Failed to get brand rankings: {str(e)}")
    
    def _build_rankings_query_and_params(
        self,
        target_date: date,
        device: str,
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None
    ) -> Tuple[str, List]:
        """
        Build the SQL query and params for rankings.
        """
        query = """
            SELECT
                ROW_NUMBER() OVER (ORDER BY AVG(cwv.performance_score) DESC) AS ranking_position,
                u.brand,
                AVG(cwv.performance_score) as avg_performance_score
            FROM url_core_web_vitals cwv
            INNER JOIN urls u ON cwv.url_id = u.url_id
            WHERE cwv.execution_date = %s
                AND u.device = %s
                AND cwv.performance_score IS NOT NULL
                AND u.brand IS NOT NULL
        """

        params: List = [target_date, device]

        # Add optional filters
        if countries:
            placeholders = ",".join(["%s"] * len(countries))
            query += f" AND u.country_id IN ({placeholders})"
            params.extend(countries)

        if page_types:
            placeholders = ",".join(["%s"] * len(page_types))
            query += f" AND u.page_type IN ({placeholders})"
            params.extend(page_types)

        query += """
            GROUP BY u.brand
            ORDER BY avg_performance_score DESC
        """

        return query, params

    def _build_brand_time_series_query_and_params(
        self,
        start_date: date,
        end_date: date,
        device: str,
        brands: List[str],
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
    ) -> Tuple[str, List]:
        """
        Build the SQL query and params for brand time series.
        """
        query = """
            SELECT
                cwv.execution_date,
                u.brand,
                AVG(cwv.performance_score) as avg_performance_score
            FROM url_core_web_vitals cwv
            INNER JOIN urls u ON cwv.url_id = u.url_id
            WHERE cwv.execution_date BETWEEN %s AND %s
                AND u.device = %s
                AND cwv.performance_score IS NOT NULL
        """

        params: List = [start_date, end_date, device]

        # Add brand filter
        if brands:
            placeholders = ",".join(["%s"] * len(brands))
            query += f" AND u.brand IN ({placeholders})"
            params.extend(brands)

        # Add optional filters
        if countries:
            placeholders = ",".join(["%s"] * len(countries))
            query += f" AND u.country_id IN ({placeholders})"
            params.extend(countries)

        if page_types:
            placeholders = ",".join(["%s"] * len(page_types))
            query += f" AND u.page_type IN ({placeholders})"
            params.extend(page_types)

        query += """
            GROUP BY cwv.execution_date, u.brand
            ORDER BY cwv.execution_date ASC, u.brand ASC
        """

        return query, params

    def get_brand_time_series(
        self,
        start_date: date,
        end_date: date,
        device: str,
        brands: List[str],
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Get performance score time series data for specific brands."""
        query, params = self._build_brand_time_series_query_and_params(
            start_date, end_date, device, brands, countries, page_types
        )

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            return [
                {
                    "execution_date": row["execution_date"],
                    "brand": row["brand"],
                    "avg_performance_score": (
                        float(row["avg_performance_score"])
                        if row["avg_performance_score"] is not None
                        else None
                    ),
                }
                for row in results
            ]

        except MySQLError as e:
            raise RuntimeError(f"Failed to get brand time series: {str(e)}")
