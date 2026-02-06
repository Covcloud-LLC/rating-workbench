"""Base mapper interface for policy model transformations."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..models.policy_transaction import PolicyTransactionCommon

# Type variable for custom model types
CustomModelT = TypeVar("CustomModelT")


class PolicyMapper(ABC, Generic[CustomModelT]):
    """
    Abstract base class for policy mappers.

    Mappers handle bidirectional conversion between:
    - Custom carrier-specific models (used in API layer)
    - Common storage model (used in repository layer)

    Each carrier/product combination should have its own mapper implementation.
    """

    @abstractmethod
    def to_common(self, custom: CustomModelT) -> PolicyTransactionCommon:
        """
        Map custom carrier-specific model to common storage model.

        Args:
            custom: Carrier-specific model instance

        Returns:
            Common storage model instance
        """
        pass

    @abstractmethod
    def to_custom(self, common: PolicyTransactionCommon) -> CustomModelT:
        """
        Map common storage model to custom carrier-specific model.

        Args:
            common: Common storage model instance

        Returns:
            Carrier-specific model instance
        """
        pass

    @property
    @abstractmethod
    def carrier_code(self) -> str:
        """
        Return the carrier code this mapper handles.

        Returns:
            Carrier code string (e.g., "ACME", "STATE_FARM")
        """
        pass

    @property
    @abstractmethod
    def product_code(self) -> str:
        """
        Return the product code this mapper handles.

        Returns:
            Product code string (e.g., "COMMERCIAL_PACKAGE", "PERSONAL_AUTO")
        """
        pass
