"""Abstract base repository interface."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract repository interface for data access operations."""

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """
        Retrieve a single item by ID.

        Args:
            id: Unique identifier for the item

        Returns:
            The item if found, None otherwise
        """
        pass

    @abstractmethod
    async def list(
        self, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """
        List items with pagination and optional filtering.

        Args:
            skip: Number of items to skip (offset)
            limit: Maximum number of items to return
            filters: Optional dictionary of field filters

        Returns:
            List of items matching the criteria
        """
        pass

    @abstractmethod
    async def create(self, item: T) -> T:
        """
        Create a new item.

        Args:
            item: The item to create

        Returns:
            The created item with generated ID
        """
        pass

    @abstractmethod
    async def update(self, id: str, item: T) -> Optional[T]:
        """
        Update an existing item.

        Args:
            id: Unique identifier for the item
            item: The updated item data

        Returns:
            The updated item if found, None otherwise
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """
        Delete an item by ID.

        Args:
            id: Unique identifier for the item

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count items matching optional filters.

        Args:
            filters: Optional dictionary of field filters

        Returns:
            Number of items matching the criteria
        """
        pass

    @abstractmethod
    async def exists(self, id: str) -> bool:
        """
        Check if an item exists.

        Args:
            id: Unique identifier for the item

        Returns:
            True if exists, False otherwise
        """
        pass
