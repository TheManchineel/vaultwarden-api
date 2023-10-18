from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Organization(BaseModel):
    name: str
    email: str
    user_count: int
    entries_count: int
    attachments_count: int
    attachments_size: int
    collections_count: int
    groups_count: int
    events_count: int


class User(BaseModel):
    name: str
    email: str
    created_at: datetime
    last_active: datetime
    entries_count: int
    attachments_count: int
    attachments_size: int
    organizations: dict[UUID, str]
