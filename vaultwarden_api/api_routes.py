from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from .api_auth import get_api_key
from .connections import vw_api

router = APIRouter()


@router.get("/stats")
async def status(api_key: Annotated[str, Depends(get_api_key)]) -> dict:
    try:
        users = vw_api.get_users()
        organizations = vw_api.get_organizations()
    except Exception:
        raise HTTPException(status_code=500, detail="Vaultwarden API error")

    return {
        "user_count": len(users),
        "organization_count": len(organizations),
        "total_entries": sum(map(lambda u: u.entries_count, users))
        + sum(map(lambda o: o.entries_count, organizations)),
        "total_attachments": sum(map(lambda u: u.attachments_count, users))
        + sum(map(lambda o: o.attachments_count, organizations)),
        "total_attachment_size": sum(map(lambda u: u.attachments_size, users)),
    }
