from typing import Optional
import datetime
from pydantic import BaseModel, Field


def current_datetime():
    return datetime.datetime.utcnow()


class Event(BaseModel):
    banner: Optional[str] = 'no_banner'
    date: Optional[datetime.datetime] = Field(default_factory=current_datetime)
    ends: Optional[datetime.datetime] = Field(default_factory=current_datetime)
    name: Optional[str] = 'no_name'
    description: str
    location: str
