"""Repository implementations for Core Web Vitals application."""
from src.infrastructure.repositories.mysql_url_repository import MySQLURLRepository
from src.infrastructure.repositories.mysql_core_web_vitals_repository import (
    MySQLCoreWebVitalsRepository,
)

__all__ = ['MySQLURLRepository', 'MySQLCoreWebVitalsRepository']
