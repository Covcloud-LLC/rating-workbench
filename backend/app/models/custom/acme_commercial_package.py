"""ACME Commercial Package custom model - carrier-specific fields."""

from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class PropertyType(str, Enum):
    """Property type enumeration."""

    OFFICE = "office"
    RETAIL = "retail"
    WAREHOUSE = "warehouse"
    MANUFACTURING = "manufacturing"
    RESTAURANT = "restaurant"


class CoverageType(str, Enum):
    """Coverage type enumeration."""

    GENERAL_LIABILITY = "general_liability"
    PROPERTY = "property"
    BUSINESS_INTERRUPTION = "business_interruption"
    WORKERS_COMP = "workers_comp"
    COMMERCIAL_AUTO = "commercial_auto"


class Location(BaseModel):
    """Business location information."""

    location_id: str = Field(..., description="Location identifier")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., min_length=2, max_length=2, description="State code")
    zip_code: str = Field(..., description="ZIP code")
    property_type: PropertyType = Field(..., description="Type of property")
    building_value: Decimal = Field(..., ge=0, description="Building replacement value")
    contents_value: Decimal = Field(..., ge=0, description="Contents/inventory value")
    square_footage: int = Field(..., ge=0, description="Square footage")


class Employee(BaseModel):
    """Employee classification information."""

    class_code: str = Field(..., description="Workers compensation class code")
    description: str = Field(..., description="Job description")
    num_employees: int = Field(..., ge=0, description="Number of employees")
    annual_payroll: Decimal = Field(..., ge=0, description="Annual payroll for this class")


class Coverage(BaseModel):
    """Coverage details."""

    coverage_type: CoverageType = Field(..., description="Type of coverage")
    limit: Decimal = Field(..., ge=0, description="Coverage limit")
    deductible: Optional[Decimal] = Field(None, ge=0, description="Deductible amount")
    premium: Decimal = Field(..., ge=0, description="Premium for this coverage")


class AcmeCommercialPackagePolicyBase(BaseModel):
    """Base ACME Commercial Package policy attributes."""

    # Standard fields (will map to common model)
    policy_number: str = Field(..., description="Policy number")
    effective_date: date = Field(..., description="Policy effective date")
    expiration_date: date = Field(..., description="Policy expiration date")
    transaction_type: str = Field(..., description="Transaction type")

    # Primary risk location
    risk_state: str = Field(..., min_length=2, max_length=2, description="Primary risk state")
    risk_zip: str = Field(..., description="Primary risk ZIP code")

    # Business information
    business_name: str = Field(..., description="Legal business name")
    dba_name: Optional[str] = Field(None, description="Doing business as name")
    business_type: str = Field(..., description="Type of business (LLC, Corp, etc)")
    industry_code: str = Field(..., description="Industry/NAICS code")
    years_in_business: int = Field(..., ge=0, description="Years in business")

    # Contact information
    contact_name: str = Field(..., description="Primary contact name")
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: str = Field(..., description="Contact phone")

    # ACME specific fields
    underwriter_code: str = Field(..., description="ACME underwriter code")
    underwriter_name: str = Field(..., description="Underwriter name")
    producer_code: str = Field(..., description="Producer/agent code")
    producer_name: str = Field(..., description="Producer/agent name")

    # Policy components
    locations: List[Location] = Field(..., min_length=1, description="Business locations")
    employees: List[Employee] = Field(default_factory=list, description="Employee classifications")
    coverages: List[Coverage] = Field(..., min_length=1, description="Coverage selections")

    # Financial
    total_premium: Decimal = Field(..., ge=0, description="Total package premium")
    payment_plan: str = Field(..., description="Payment plan (full_pay, monthly, quarterly)")
    commission_rate: Decimal = Field(..., ge=0, le=100, description="Commission percentage")

    # Status
    status: str = Field(..., description="Policy status")


class AcmeCommercialPackagePolicyCreate(AcmeCommercialPackagePolicyBase):
    """Schema for creating an ACME Commercial Package policy."""

    pass


class AcmeCommercialPackagePolicyUpdate(BaseModel):
    """Schema for updating an ACME Commercial Package policy (all fields optional)."""

    policy_number: Optional[str] = None
    effective_date: Optional[date] = None
    expiration_date: Optional[date] = None
    business_name: Optional[str] = None
    dba_name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    locations: Optional[List[Location]] = None
    employees: Optional[List[Employee]] = None
    coverages: Optional[List[Coverage]] = None
    total_premium: Optional[Decimal] = None
    payment_plan: Optional[str] = None
    status: Optional[str] = None


class AcmeCommercialPackagePolicy(AcmeCommercialPackagePolicyBase):
    """Complete ACME Commercial Package policy model."""

    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )

    model_config = ConfigDict(
        json_encoders={Decimal: str},
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "policy_number": "ACME-CPP-2024-001234",
                "effective_date": "2024-01-01",
                "expiration_date": "2025-01-01",
                "transaction_type": "new_business",
                "risk_state": "CA",
                "risk_zip": "90210",
                "business_name": "Acme Widgets Inc",
                "dba_name": "Acme Widgets",
                "business_type": "Corporation",
                "industry_code": "333514",
                "years_in_business": 10,
                "contact_name": "John Doe",
                "contact_email": "john.doe@acmewidgets.com",
                "contact_phone": "555-1234",
                "underwriter_code": "UW-12345",
                "underwriter_name": "Jane Underwriter",
                "producer_code": "PROD-67890",
                "producer_name": "Bob Agent",
                "locations": [],
                "employees": [],
                "coverages": [],
                "total_premium": "15000.00",
                "payment_plan": "quarterly",
                "commission_rate": "15.0",
                "status": "bound",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            }
        },
    )
