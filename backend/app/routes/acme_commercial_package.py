"""API routes for ACME Commercial Package policies."""


from fastapi import APIRouter, Depends, HTTPException, Query

from ..mappers.acme_commercial_package_mapper import AcmeCommercialPackageMapper
from ..models.custom.acme_commercial_package import (
    AcmeCommercialPackagePolicy,
    AcmeCommercialPackagePolicyCreate,
    AcmeCommercialPackagePolicyUpdate,
)
from ..repositories.json_file import JSONFileRepository
from ..services.policy_transaction_service import PolicyTransactionService

router = APIRouter(prefix="/api/acme-commercial-package", tags=["ACME Commercial Package"])


def get_service() -> PolicyTransactionService[AcmeCommercialPackagePolicy]:
    """Dependency injection for ACME Commercial Package service."""
    repository = JSONFileRepository(data_dir="./data")
    mapper = AcmeCommercialPackageMapper()
    return PolicyTransactionService(repository, mapper)


@router.get("/policies", response_model=list[AcmeCommercialPackagePolicy])
async def list_policies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    carrier_code: str | None = Query(None, description="Filter by carrier code"),
    status: str | None = Query(None, description="Filter by status"),
    service: PolicyTransactionService[AcmeCommercialPackagePolicy] = Depends(get_service),
) -> list[AcmeCommercialPackagePolicy]:
    """
    List ACME Commercial Package policies with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100)
    - **carrier_code**: Optional filter by carrier
    - **status**: Optional filter by status
    """
    filters = {}
    if carrier_code:
        filters["carrier_code"] = carrier_code
    if status:
        filters["status"] = status

    return await service.list(skip=skip, limit=limit, filters=filters if filters else None)


@router.get("/policies/{policy_id}", response_model=AcmeCommercialPackagePolicy)
async def get_policy(
    policy_id: str,
    service: PolicyTransactionService[AcmeCommercialPackagePolicy] = Depends(get_service),
) -> AcmeCommercialPackagePolicy:
    """
    Get a specific ACME Commercial Package policy by ID.

    - **policy_id**: Unique policy identifier
    """
    policy = await service.get(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.post("/policies", response_model=AcmeCommercialPackagePolicy, status_code=201)
async def create_policy(
    policy: AcmeCommercialPackagePolicyCreate,
    service: PolicyTransactionService[AcmeCommercialPackagePolicy] = Depends(get_service),
) -> AcmeCommercialPackagePolicy:
    """
    Create a new ACME Commercial Package policy.

    The policy data will be mapped to the common storage model and persisted.
    """
    # Convert create model to full model for service
    policy_dict = policy.model_dump()
    policy_dict["id"] = None  # Will be generated
    full_policy = AcmeCommercialPackagePolicy(**policy_dict)

    return await service.create(full_policy)


@router.put("/policies/{policy_id}", response_model=AcmeCommercialPackagePolicy)
async def update_policy(
    policy_id: str,
    policy_update: AcmeCommercialPackagePolicyUpdate,
    service: PolicyTransactionService[AcmeCommercialPackagePolicy] = Depends(get_service),
) -> AcmeCommercialPackagePolicy:
    """
    Update an existing ACME Commercial Package policy.

    - **policy_id**: Unique policy identifier
    - Only provided fields will be updated
    """
    # Get existing policy
    existing = await service.get(policy_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Policy not found")

    # Apply updates
    update_data = policy_update.model_dump(exclude_unset=True)
    updated_policy = existing.model_copy(update=update_data)

    result = await service.update(policy_id, updated_policy)
    if not result:
        raise HTTPException(status_code=404, detail="Policy not found")

    return result


@router.delete("/policies/{policy_id}", status_code=204)
async def delete_policy(
    policy_id: str,
    service: PolicyTransactionService[AcmeCommercialPackagePolicy] = Depends(get_service),
):
    """
    Delete an ACME Commercial Package policy.

    - **policy_id**: Unique policy identifier
    """
    deleted = await service.delete(policy_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Policy not found")


@router.get("/policies/count", response_model=dict)
async def count_policies(
    carrier_code: str | None = Query(None, description="Filter by carrier code"),
    status: str | None = Query(None, description="Filter by status"),
    service: PolicyTransactionService[AcmeCommercialPackagePolicy] = Depends(get_service),
) -> dict:
    """
    Count ACME Commercial Package policies.

    - **carrier_code**: Optional filter by carrier
    - **status**: Optional filter by status
    """
    filters = {}
    if carrier_code:
        filters["carrier_code"] = carrier_code
    if status:
        filters["status"] = status

    count = await service.count(filters if filters else None)
    return {"count": count}


@router.get("/policies/{policy_id}/exists", response_model=dict)
async def check_policy_exists(
    policy_id: str,
    service: PolicyTransactionService[AcmeCommercialPackagePolicy] = Depends(get_service),
) -> dict:
    """
    Check if a policy exists.

    - **policy_id**: Unique policy identifier
    """
    exists = await service.exists(policy_id)
    return {"exists": exists}
