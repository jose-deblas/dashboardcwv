"""
Brand repository interface.

This module defines the abstract interface for brand repository operations.
Following Clean Architecture principles, this interface is in the domain layer.
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class BrandRepository(ABC):
    """
    Abstract repository interface for brand operations.

    This interface defines methods for retrieving brand information,
    particularly target brands for dashboard filtering and visualization.
    """

    @abstractmethod
    def get_target_brands(self) -> List[str]:
        """
        Get list of target brands (brands to highlight in dashboard).

        Returns:
            List of brand names marked as target brands

        Raises:
            RuntimeError: If database query fails
        """
        pass

    @abstractmethod
    def get_target_brand_colors(self) -> Dict[str, str]:
        """
        Get color palette for target brands.

        Returns:
            Dictionary mapping brand names to hex color codes

        Raises:
            RuntimeError: If database query fails
        """
        pass
