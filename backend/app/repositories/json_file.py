"""JSON file-based repository implementation for testing/development."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from ..models.policy_transaction import PolicyTransactionCommon
from .base import BaseRepository


class JSONFileRepository(BaseRepository[PolicyTransactionCommon]):
    """Repository implementation using JSON files."""

    def __init__(self, data_dir: str = "./data"):
        """
        Initialize the JSON file repository.

        Args:
            data_dir: Directory path for storing JSON files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "policy_transactions.json"
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensure the data file exists."""
        if not self.file_path.exists():
            self._write_data([])

    def _read_data(self) -> list[dict[str, Any]]:
        """Read all data from JSON file."""
        try:
            with open(self.file_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: list[dict[str, Any]]):
        """Write all data to JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _to_dict(self, policy_transaction: PolicyTransactionCommon) -> dict[str, Any]:
        """Convert PolicyTransactionCommon to dictionary."""
        return policy_transaction.model_dump(mode="json")

    def _from_dict(self, data: dict[str, Any]) -> PolicyTransactionCommon:
        """Convert dictionary to PolicyTransactionCommon."""
        return PolicyTransactionCommon(**data)

    def _matches_filters(self, item: dict[str, Any], filters: dict[str, Any]) -> bool:
        """Check if item matches all filters."""
        for key, value in filters.items():
            if key not in item:
                return False
            if isinstance(value, list):
                # Check if item value is in the list
                if item[key] not in value:
                    return False
            elif item[key] != value:
                return False
        return True

    async def get(self, id: str) -> PolicyTransactionCommon | None:
        """Get a policy transaction by ID."""
        data = self._read_data()
        for item in data:
            if item.get("id") == id:
                return self._from_dict(item)
        return None

    async def list(
        self, skip: int = 0, limit: int = 100, filters: dict[str, Any] | None = None
    ) -> list[PolicyTransactionCommon]:
        """List policy transactions with pagination and filtering."""
        data = self._read_data()

        # Apply filters
        if filters:
            data = [item for item in data if self._matches_filters(item, filters)]

        # Apply pagination
        paginated = data[skip : skip + limit]

        return [self._from_dict(item) for item in paginated]

    async def create(self, item: PolicyTransactionCommon) -> PolicyTransactionCommon:
        """Create a new policy transaction."""
        data = self._read_data()

        # Generate ID if not present
        if not item.id:
            item.id = str(uuid.uuid4())

        # Set timestamps
        now = datetime.utcnow()
        item.created_at = now
        item.updated_at = now

        # Add to data
        data.append(self._to_dict(item))
        self._write_data(data)

        return item

    async def update(
        self, id: str, item: PolicyTransactionCommon
    ) -> PolicyTransactionCommon | None:
        """Update an existing policy transaction."""
        data = self._read_data()

        for i, existing in enumerate(data):
            if existing.get("id") == id:
                # Update timestamp
                item.id = id
                item.updated_at = datetime.utcnow()
                # Preserve created_at from existing
                item.created_at = datetime.fromisoformat(
                    existing["created_at"].replace("Z", "+00:00")
                )

                data[i] = self._to_dict(item)
                self._write_data(data)
                return item

        return None

    async def delete(self, id: str) -> bool:
        """Delete a policy transaction by ID."""
        data = self._read_data()
        original_len = len(data)

        data = [item for item in data if item.get("id") != id]

        if len(data) < original_len:
            self._write_data(data)
            return True

        return False

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count policy transactions matching filters."""
        data = self._read_data()

        if filters:
            data = [item for item in data if self._matches_filters(item, filters)]

        return len(data)

    async def exists(self, id: str) -> bool:
        """Check if a policy transaction exists."""
        data = self._read_data()
        return any(item.get("id") == id for item in data)
