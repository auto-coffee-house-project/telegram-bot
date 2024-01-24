from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

__all__ = ('Invitation',)


class Invitation(BaseModel):
    id: UUID
    created_at: datetime
    expires_at: datetime
