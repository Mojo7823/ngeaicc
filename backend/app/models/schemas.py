from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class TestCaseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)

class TestCase(TestCaseBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    manufacturer: Optional[str] = Field(None, max_length=255)
    model: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    manufacturer: Optional[str] = Field(None, max_length=255)
    model: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None

class Device(DeviceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# TOE Description schemas
class TOEDescriptionBase(BaseModel):
    toe_name: Optional[str] = Field(None, max_length=255)
    toe_vendor: Optional[str] = Field(None, max_length=255)
    evaluation_date: Optional[str] = Field(None, max_length=100)
    laboratory_address: Optional[str] = Field(None, max_length=500)
    laboratory_name: Optional[str] = Field(None, max_length=255)
    toe_version: Optional[str] = Field(None, max_length=100)
    common_criteria_version: Optional[str] = Field(None, max_length=100)
    vendor_address: Optional[str] = None  # HTML content
    evaluation_personnel: Optional[str] = None  # HTML content
    protection_profile_module: Optional[str] = None  # HTML content
    toe_description: Optional[str] = None  # HTML content

class TOEDescriptionCreate(TOEDescriptionBase):
    pass

class TOEDescriptionUpdate(TOEDescriptionBase):
    pass

class TOEDescription(TOEDescriptionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class HelloWorldResponse(BaseModel):
    message: str
    timestamp: datetime
    data: Optional[dict] = None

class MessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: Optional[str] = None

# Admin schemas
class AdminStats(BaseModel):
    system: dict
    database: dict
    api: dict

class DatabaseTable(BaseModel):
    schema: str
    name: str
    size: str
    statistics: dict

class DatabaseHealth(BaseModel):
    status: str
    connection: str
    pgvector_enabled: bool
    database_version: str
    last_check: datetime

class ApiEndpoint(BaseModel):
    path: str
    method: str
    description: str
    category: str

class SystemInfo(BaseModel):
    application: dict
    database: dict
    frontend: dict
    deployment: dict
    timestamp: datetime
