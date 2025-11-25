"""
MySQL implementation of brand repository.

This module implements the BrandRepository interface for MySQL database.
Following Clean Architecture principles with proper dependency injection.
"""

from typing import Dict, List

from mysql.connector import Error as MySQLError

from src.domain.repositories.brand_repository import BrandRepository
from src.infrastructure.database.connection import DatabaseConnection


class MySQLBrandRepository(BrandRepository):
    """
    MySQL implementation of brand repository.

    This repository handles brand-related queries including target brands
    and their color configurations for dashboard visualizations.
    """

    def __init__(self, db_connection: DatabaseConnection):
        """
        Initialize repository with database connection.

        Args:
            db_connection: Database connection instance for dependency injection
        """
        self._db = db_connection

    def get_target_brands(self) -> List[str]:
        """
        Get list of target brands from database.

        Executes query: SELECT brand FROM url_brands WHERE target_brand=TRUE ORDER BY brand

        Returns:
            List of brand names marked as target brands

        Raises:
            RuntimeError: If database query fails
        """
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
            raise RuntimeError(f"Failed to get target brands: {str(e)}")

    def get_target_brand_colors(self) -> Dict[str, str]:
        """
        Get color palette for target brands from database.

        Expects url_brands table to have a 'brand_color' column with hex color codes.

        Returns:
            Dictionary mapping brand names to hex color codes

        Raises:
            RuntimeError: If database query fails
        """
        query = """
            SELECT brand, brand_color
            FROM url_brands
            WHERE target_brand = TRUE
                AND brand_color IS NOT NULL
            ORDER BY brand ASC
        """

        try:
            connection = self._db.get_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            return {row[0]: row[1] for row in results if row[0] and row[1]}

        except MySQLError as e:
            raise RuntimeError(f"Failed to get target brand colors: {str(e)}")
