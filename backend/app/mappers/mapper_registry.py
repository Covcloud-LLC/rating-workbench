"""Mapper registry for managing and retrieving mappers by carrier/product."""


from .base import PolicyMapper


class MapperRegistry:
    """
    Registry for policy mappers.

    Allows registration and retrieval of mappers by carrier and product code.
    Provides a centralized way to manage all mapper implementations.
    """

    def __init__(self):
        """Initialize the mapper registry."""
        self._mappers: dict[tuple[str, str], type[PolicyMapper]] = {}

    def register(self, mapper_class: type[PolicyMapper]) -> None:
        """
        Register a mapper class.

        Args:
            mapper_class: Mapper class to register

        Raises:
            ValueError: If a mapper for this carrier/product is already registered
        """
        # Instantiate temporarily to get carrier/product codes
        instance = mapper_class()
        key = (instance.carrier_code, instance.product_code)

        if key in self._mappers:
            raise ValueError(
                f"Mapper already registered for carrier={instance.carrier_code}, "
                f"product={instance.product_code}"
            )

        self._mappers[key] = mapper_class

    def get_mapper(self, carrier_code: str, product_code: str) -> PolicyMapper:
        """
        Get a mapper instance for the specified carrier and product.

        Args:
            carrier_code: Carrier code (e.g., "ACME")
            product_code: Product code (e.g., "COMMERCIAL_PACKAGE")

        Returns:
            Mapper instance for the carrier/product

        Raises:
            KeyError: If no mapper is registered for the carrier/product
        """
        key = (carrier_code, product_code)

        if key not in self._mappers:
            raise KeyError(
                f"No mapper registered for carrier={carrier_code}, product={product_code}. "
                f"Available mappers: {list(self._mappers.keys())}"
            )

        mapper_class = self._mappers[key]
        return mapper_class()

    def get_mapper_by_policy(self, policy_number: str) -> PolicyMapper | None:
        """
        Get a mapper based on policy number prefix or pattern.

        This is a convenience method for scenarios where you need to determine
        the mapper from the policy number format.

        Args:
            policy_number: Policy number to analyze

        Returns:
            Mapper instance if pattern matches, None otherwise

        Note:
            This is a simple prefix-based implementation. Override or enhance
            as needed for more sophisticated policy number parsing.
        """
        # Simple prefix-based detection
        if policy_number.startswith("ACME-"):
            return self.get_mapper("ACME", "COMMERCIAL_PACKAGE")
        # Add more patterns as needed
        return None

    def list_registered(self) -> list[tuple[str, str]]:
        """
        List all registered carrier/product combinations.

        Returns:
            List of (carrier_code, product_code) tuples
        """
        return list(self._mappers.keys())

    def clear(self) -> None:
        """Clear all registered mappers (useful for testing)."""
        self._mappers.clear()


# Global registry instance
_global_registry = MapperRegistry()


def get_global_registry() -> MapperRegistry:
    """
    Get the global mapper registry instance.

    Returns:
        Global mapper registry
    """
    return _global_registry


def register_mapper(mapper_class: type[PolicyMapper]) -> None:
    """
    Register a mapper in the global registry.

    Args:
        mapper_class: Mapper class to register
    """
    _global_registry.register(mapper_class)
