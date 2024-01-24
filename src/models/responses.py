from pydantic import BaseModel

__all__ = ('APIResponse',)


class APIResponse(BaseModel):
    ok: bool = False
    message: str | None = None
    result: dict | list | None = None
    extra: dict | None = None
