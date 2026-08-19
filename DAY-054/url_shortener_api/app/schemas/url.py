from datetime import datetime
from pydantic import BaseModel, HttpUrl, ConfigDict


class URLCreate(BaseModel):
    """
    Request schema for creating a shortened URL.
    """
    original_url: HttpUrl


class URLResponse(BaseModel):
    """
    Response schema after creating a shortened URL.
    """
    id: int
    original_url: HttpUrl
    short_code: str
    short_url: str
    model_config = ConfigDict(from_attributes=True)


class URLStats(BaseModel):
    """
    Response schema for URL statistics.
    """
    original_url: HttpUrl
    short_code: str
    clicks: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)