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

class HelloWorldResponse(BaseModel):
    message: str
    timestamp: datetime
    data: Optional[dict] = None

class MessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: Optional[str] = None
