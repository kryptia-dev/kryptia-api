from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime


class Severity(str, Enum):
    Low      = "Low"
    Medium   = "Medium"
    High     = "High"
    Critical = "Critical"


class Patch(SQLModel, table=True):
    id:         int       = Field(primary_key=True)
    name:       str
    severity:   Severity
    product:    str
    created_at: datetime  = Field(default_factory=datetime.utcnow)

