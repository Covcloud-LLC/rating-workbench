"""Mapper for ACME Commercial Package policies."""

from datetime import datetime
from decimal import Decimal
from typing import Dict, Any

from .base import PolicyMapper
from ..models.policy_transaction import PolicyTransactionCommon
from ..models.custom.acme_commercial_package import (
    AcmeCommercialPackagePolicy,
    Location,
    Employee,
    Coverage,
)


class AcmeCommercialPackageMapper(PolicyMapper[AcmeCommercialPackagePolicy]):
    """Mapper for ACME Commercial Package policies."""

    @property
    def carrier_code(self) -> str:
        """Return carrier code."""
        return "ACME"

    @property
    def product_code(self) -> str:
        """Return product code."""
        return "COMMERCIAL_PACKAGE"

    def to_common(self, custom: AcmeCommercialPackagePolicy) -> PolicyTransactionCommon:
        """
        Map ACME Commercial Package policy to common storage model.

        Args:
            custom: ACME Commercial Package policy

        Returns:
            Common storage model
        """
        # Serialize complex nested objects to custom_fields
        custom_fields = self._serialize_custom_fields(custom)

        return PolicyTransactionCommon(
            id=custom.id if hasattr(custom, "id") else None,
            policy_number=custom.policy_number,
            transaction_type=custom.transaction_type,
            effective_date=custom.effective_date,
            expiration_date=custom.expiration_date,
            carrier_code=self.carrier_code,
            product_code=self.product_code,
            premium=custom.total_premium,
            currency="USD",
            risk_state=custom.risk_state,
            risk_zip=custom.risk_zip,
            status=custom.status,
            custom_fields=custom_fields,
            created_at=custom.created_at if hasattr(custom, "created_at") else datetime.utcnow(),
            updated_at=custom.updated_at if hasattr(custom, "updated_at") else datetime.utcnow(),
        )

    def to_custom(self, common: PolicyTransactionCommon) -> AcmeCommercialPackagePolicy:
        """
        Map common storage model to ACME Commercial Package policy.

        Args:
            common: Common storage model

        Returns:
            ACME Commercial Package policy
        """
        # Deserialize custom_fields back to complex objects
        custom_data = self._deserialize_custom_fields(common.custom_fields)

        return AcmeCommercialPackagePolicy(
            id=common.id,
            policy_number=common.policy_number,
            effective_date=common.effective_date,
            expiration_date=common.expiration_date,
            transaction_type=common.transaction_type,
            risk_state=common.risk_state,
            risk_zip=common.risk_zip,
            business_name=custom_data.get("business_name", ""),
            dba_name=custom_data.get("dba_name"),
            business_type=custom_data.get("business_type", ""),
            industry_code=custom_data.get("industry_code", ""),
            years_in_business=custom_data.get("years_in_business", 0),
            contact_name=custom_data.get("contact_name", ""),
            contact_email=custom_data.get("contact_email"),
            contact_phone=custom_data.get("contact_phone", ""),
            underwriter_code=custom_data.get("underwriter_code", ""),
            underwriter_name=custom_data.get("underwriter_name", ""),
            producer_code=custom_data.get("producer_code", ""),
            producer_name=custom_data.get("producer_name", ""),
            locations=custom_data.get("locations", []),
            employees=custom_data.get("employees", []),
            coverages=custom_data.get("coverages", []),
            total_premium=common.premium,
            payment_plan=custom_data.get("payment_plan", "quarterly"),
            commission_rate=custom_data.get("commission_rate", Decimal("0.0")),
            status=common.status,
            created_at=common.created_at,
            updated_at=common.updated_at,
        )

    def _serialize_custom_fields(self, custom: AcmeCommercialPackagePolicy) -> Dict[str, Any]:
        """
        Serialize ACME-specific fields to dictionary for storage.

        Args:
            custom: ACME Commercial Package policy

        Returns:
            Dictionary of custom fields
        """
        return {
            # Business information
            "business_name": custom.business_name,
            "dba_name": custom.dba_name,
            "business_type": custom.business_type,
            "industry_code": custom.industry_code,
            "years_in_business": custom.years_in_business,
            # Contact information
            "contact_name": custom.contact_name,
            "contact_email": custom.contact_email,
            "contact_phone": custom.contact_phone,
            # ACME-specific personnel
            "underwriter_code": custom.underwriter_code,
            "underwriter_name": custom.underwriter_name,
            "producer_code": custom.producer_code,
            "producer_name": custom.producer_name,
            # Complex nested objects (serialized to JSON)
            "locations": [loc.model_dump(mode="json") for loc in custom.locations],
            "employees": [emp.model_dump(mode="json") for emp in custom.employees],
            "coverages": [cov.model_dump(mode="json") for cov in custom.coverages],
            # Financial details
            "payment_plan": custom.payment_plan,
            "commission_rate": str(custom.commission_rate),
        }

    def _deserialize_custom_fields(self, custom_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deserialize custom fields dictionary back to typed objects.

        Args:
            custom_fields: Dictionary of custom fields from storage

        Returns:
            Dictionary with deserialized complex objects
        """
        # Deserialize complex nested objects
        locations = [Location(**loc) for loc in custom_fields.get("locations", [])]
        employees = [Employee(**emp) for emp in custom_fields.get("employees", [])]
        coverages = [Coverage(**cov) for cov in custom_fields.get("coverages", [])]

        return {
            # Business information
            "business_name": custom_fields.get("business_name", ""),
            "dba_name": custom_fields.get("dba_name"),
            "business_type": custom_fields.get("business_type", ""),
            "industry_code": custom_fields.get("industry_code", ""),
            "years_in_business": custom_fields.get("years_in_business", 0),
            # Contact information
            "contact_name": custom_fields.get("contact_name", ""),
            "contact_email": custom_fields.get("contact_email"),
            "contact_phone": custom_fields.get("contact_phone", ""),
            # ACME-specific personnel
            "underwriter_code": custom_fields.get("underwriter_code", ""),
            "underwriter_name": custom_fields.get("underwriter_name", ""),
            "producer_code": custom_fields.get("producer_code", ""),
            "producer_name": custom_fields.get("producer_name", ""),
            # Complex objects (now deserialized)
            "locations": locations,
            "employees": employees,
            "coverages": coverages,
            # Financial details
            "payment_plan": custom_fields.get("payment_plan", "quarterly"),
            "commission_rate": Decimal(custom_fields.get("commission_rate", "0.0")),
        }
