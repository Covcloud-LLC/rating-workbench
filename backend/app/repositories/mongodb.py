"""MongoDB repository implementation."""

from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING

from .base import BaseRepository
from ..models.policy_transaction import PolicyTransactionCommon


class MongoDBRepository(BaseRepository[PolicyTransactionCommon]):
    """Repository implementation using MongoDB."""

    def __init__(self, connection_url: str, database_name: str = "rating_workbench"):
        """
        Initialize MongoDB repository.

        Args:
            connection_url: MongoDB connection URL
            database_name: Name of the database to use
        """
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(connection_url)
        self.db: AsyncIOMotorDatabase = self.client[database_name]
        self.collection = self.db["policy_transactions"]

    async def close(self):
        """Close the database connection."""
        self.client.close()

    def _to_dict(self, policy_transaction: PolicyTransactionCommon) -> Dict[str, Any]:
        """Convert PolicyTransactionCommon to MongoDB document."""
        doc = policy_transaction.model_dump(mode="json")
        # MongoDB uses _id instead of id
        doc["_id"] = doc.pop("id")
        return doc

    def _from_dict(self, doc: Dict[str, Any]) -> PolicyTransactionCommon:
        """Convert MongoDB document to PolicyTransactionCommon."""
        if "_id" in doc:
            doc["id"] = str(doc.pop("_id"))
        return PolicyTransactionCommon(**doc)

    def _build_filter(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build MongoDB filter from filters dict."""
        if not filters:
            return {}

        mongo_filter = {}
        for key, value in filters.items():
            if isinstance(value, list):
                # Convert list to $in operator
                mongo_filter[key] = {"$in": value}
            else:
                mongo_filter[key] = value

        return mongo_filter

    async def get(self, id: str) -> Optional[PolicyTransactionCommon]:
        """Get a policy transaction by ID."""
        doc = await self.collection.find_one({"_id": id})
        if doc:
            return self._from_dict(doc)
        return None

    async def list(
        self, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None
    ) -> List[PolicyTransactionCommon]:
        """List policy transactions with pagination and filtering."""
        mongo_filter = self._build_filter(filters)

        cursor = (
            self.collection.find(mongo_filter)
            .skip(skip)
            .limit(limit)
            .sort("created_at", DESCENDING)
        )

        results = []
        async for doc in cursor:
            results.append(self._from_dict(doc))

        return results

    async def create(self, item: PolicyTransactionCommon) -> PolicyTransactionCommon:
        """Create a new policy transaction."""
        # Generate ID if not present
        if not item.id:
            item.id = str(uuid.uuid4())

        # Set timestamps
        now = datetime.utcnow()
        item.created_at = now
        item.updated_at = now

        doc = self._to_dict(item)
        await self.collection.insert_one(doc)

        return item

    async def update(
        self, id: str, item: PolicyTransactionCommon
    ) -> Optional[PolicyTransactionCommon]:
        """Update an existing policy transaction."""
        # Preserve ID and created_at
        item.id = id
        item.updated_at = datetime.utcnow()

        # Get existing document to preserve created_at
        existing = await self.collection.find_one({"_id": id})
        if not existing:
            return None

        item.created_at = existing.get("created_at", item.created_at)

        doc = self._to_dict(item)
        result = await self.collection.replace_one({"_id": id}, doc)

        if result.modified_count > 0:
            return item

        return None

    async def delete(self, id: str) -> bool:
        """Delete a policy transaction by ID."""
        result = await self.collection.delete_one({"_id": id})
        return result.deleted_count > 0

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count policy transactions matching filters."""
        mongo_filter = self._build_filter(filters)
        return await self.collection.count_documents(mongo_filter)

    async def exists(self, id: str) -> bool:
        """Check if a policy transaction exists."""
        count = await self.collection.count_documents({"_id": id}, limit=1)
        return count > 0

    async def create_indexes(self):
        """Create database indexes for better performance."""
        # Index on created_at for sorting
        await self.collection.create_index([("created_at", DESCENDING)])
        # Index on category for filtering
        await self.collection.create_index([("category", ASCENDING)])
        # Index on score for filtering/sorting
        await self.collection.create_index([("score", DESCENDING)])
        # Text index for searching title and description
        await self.collection.create_index([("title", "text"), ("description", "text")])
