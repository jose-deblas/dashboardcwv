"""Database connection management for MySQL."""
import os
from typing import Optional
import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from src.domain.exceptions import DatabaseConnectionException


class DatabaseConnection:
    """Manages MySQL database connections with connection pooling."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """
        Initialize database connection parameters.

        Args:
            host: MySQL host (defaults to MYSQL_HOST env var)
            port: MySQL port (defaults to MYSQL_PORT env var)
            database: Database name (defaults to MYSQL_DATABASE env var)
            user: Database user (defaults to MYSQL_USER env var)
            password: Database password (defaults to MYSQL_PASSWORD env var)
        """
        self.host = host or os.getenv('MYSQL_HOST', 'mysql')
        self.port = port or int(os.getenv('MYSQL_PORT', '3306'))
        self.database = database or os.getenv('MYSQL_DATABASE', 'core_web_vitals')
        self.user = user or os.getenv('MYSQL_USER', 'cwv_user')
        self.password = password or os.getenv('MYSQL_PASSWORD', 'cwv_password')
        self._connection: Optional[MySQLConnection | PooledMySQLConnection] = None

    def connect(self) -> MySQLConnection | PooledMySQLConnection:
        """
        Establish a database connection.

        Returns:
            MySQL connection object

        Raises:
            DatabaseConnectionException: If connection fails
        """
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    autocommit=False,
                )
            return self._connection
        except Error as e:
            raise DatabaseConnectionException(
                f"Failed to connect to database: {e}"
            ) from e

    def disconnect(self) -> None:
        """Close the database connection."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None

    def get_connection(self) -> MySQLConnection | PooledMySQLConnection:
        """
        Get or create a database connection.

        Returns:
            MySQL connection object

        Raises:
            DatabaseConnectionException: If connection fails
        """
        return self.connect()

    def __enter__(self) -> MySQLConnection | PooledMySQLConnection:
        """Context manager entry."""
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """Context manager exit."""
        self.disconnect()
