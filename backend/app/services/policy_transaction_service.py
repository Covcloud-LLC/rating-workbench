"""Policy transaction service - uses mapper layer for model transformations."""

from typing import Optional, List, Dict, Any, Generic, TypeVar

from ..repositories.base import BaseRepository
from ..models.policy_transaction import PolicyTransactionCommon
from ..mappers.base import PolicyMapper

# Type variable for custom model types
CustomModelT = TypeVar("CustomModelT")


class PolicyTransactionService(Generic[CustomModelT]):
    """
    Service layer for policy transactions.
    Delegates mapping to dedicated mapper classes for separation of concerns.
    """

    def __init__(
        self,
        repository: BaseRepository[PolicyTransactionCommon],
        mapper: PolicyMapper[CustomModelT],
    ):
        """
        Initialize the service with a repository and mapper.

        Args:
            repository: Repository implementation for data access
            mapper: Mapper implementation for model transformations
        """
        self.repository = repository
        self.mapper = mapper

    async def get(self, id: str) -> Optional[CustomModelT]:
        """
        Get a policy transaction by ID.

        Args:
            id: Policy transaction ID

        Returns:
            Custom model if found, None otherwise
        """
        common = await self.repository.get(id)
        if common:
            return self.mapper.to_custom(common)
        return None

    async def list(
        self, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None
    ) -> List[CustomModelT]:
        """
        List policy transactions with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filters

        Returns:
            List of custom models
        """
        common_list = await self.repository.list(skip, limit, filters)
        return [self.mapper.to_custom(common) for common in common_list]

    async def create(self, custom_model: CustomModelT) -> CustomModelT:
        """
        Create a new policy transaction.

        Args:
            custom_model: Custom model to create

        Returns:
            Created custom model with ID
        """
        common = self.mapper.to_common(custom_model)
        created = await self.repository.create(common)
        return self.mapper.to_custom(created)

    async def update(self, id: str, custom_model: CustomModelT) -> Optional[CustomModelT]:
        """
        Update an existing policy transaction.

        Args:
            id: Policy transaction ID
            custom_model: Updated custom model

        Returns:
            Updated custom model if found, None otherwise
        """
        common = self.mapper.to_common(custom_model)
        updated = await self.repository.update(id, common)
        if updated:
            return self.mapper.to_custom(updated)
        return None

    async def delete(self, id: str) -> bool:
        """
        Delete a policy transaction.

        Args:
            id: Policy transaction ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(id)

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count policy transactions.

        Args:
            filters: Optional filters

        Returns:
            Count of matching records
        """
        return await self.repository.count(filters)

    async def exists(self, id: str) -> bool:
        """
        Check if a policy transaction exists.

        Args:
            id: Policy transaction ID

        Returns:
            True if exists, False otherwise
        """
        return await self.repository.exists(id)
