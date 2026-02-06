"""PolicyTransaction common model - used for storage across all NoSQL backends."""

from datetime import datetime, date
from typing import Optional, Dict, Any
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class PolicyTransactionCommon(BaseModel):
    """
    Common storage model for policy transactions.
    This model contains fields that are standardized across all carriers.
    Carrier-specific fields are stored in the 'custom_fields' dictionary.
    """

    # Identity
    id: Optional[str] = Field(None, description="Unique identifier")
    policy_number: str = Field(..., min_length=1, max_length=100, description="Policy number")

    # Transaction metadata
    transaction_type: str = Field(
        ..., description="Type of transaction (new_business, renewal, endorsement, cancellation)"
    )
    effective_date: date = Field(..., description="Policy effective date")
    expiration_date: date = Field(..., description="Policy expiration date")
    transaction_date: datetime = Field(
        default_factory=datetime.utcnow, description="Transaction timestamp"
    )

    # Carrier and product info
    carrier_code: str = Field(
        ..., min_length=1, max_length=50, description="Insurance carrier code"
    )
    product_code: str = Field(
        ..., min_length=1, max_length=50, description="Product/line of business code"
    )

    # Financial
    premium: Decimal = Field(..., ge=0, description="Total premium amount")
    currency: str = Field(default="USD", max_length=3, description="Currency code")

    # Risk information
    risk_state: str = Field(..., min_length=2, max_length=2, description="State/province code")
    risk_zip: Optional[str] = Field(None, max_length=10, description="ZIP/postal code")

    # Status
    status: str = Field(..., description="Transaction status (quoted, bound, issued, cancelled)")

    # Custom carrier-specific fields stored as JSON
    custom_fields: Dict[str, Any] = Field(
        default_factory=dict, description="Carrier-specific custom fields"
    )

    # System metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )
    created_by: Optional[str] = Field(None, description="User who created the record")
    updated_by: Optional[str] = Field(None, description="User who last updated the record")

    model_config = ConfigDict(
        json_encoders={Decimal: str},
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "policy_number": "AUTO-2024-001234",
                "transaction_type": "new_business",
                "effective_date": "2024-01-01",
                "expiration_date": "2025-01-01",
                "carrier_code": "STATE_FARM",
                "product_code": "PERSONAL_AUTO",
                "premium": "1250.00",
                "currency": "USD",
                "risk_state": "CA",
                "risk_zip": "90210",
                "status": "bound",
                "custom_fields": {},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            }
        },
    )
