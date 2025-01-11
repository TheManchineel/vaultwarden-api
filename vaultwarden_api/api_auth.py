from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from os import getenv

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_dependency = Annotated[str, Depends(api_key_header)]

API_KEY = getenv("API_KEY", "")
if not API_KEY:
    print("⚠️ WARNING: API_KEY is not specified in the environment. The API will be open to the public. 😱")


async def get_api_key(api_key: api_key_dependency):
    if not API_KEY or api_key == API_KEY:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")
