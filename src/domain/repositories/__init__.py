"""Repository interfaces for Core Web Vitals application."""
from src.domain.repositories.url_repository import URLRepository
from src.domain.repositories.core_web_vitals_repository import CoreWebVitalsRepository

__all__ = ['URLRepository', 'CoreWebVitalsRepository']
