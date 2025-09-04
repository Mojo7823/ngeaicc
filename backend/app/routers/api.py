from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List

from app.database import get_db, TestCase as TestCaseModel, Device as DeviceModel
from app.models.schemas import (
    HelloWorldResponse, 
    MessageRequest,
    TestCase, 
    TestCaseCreate, 
    TestCaseUpdate,
    Device,
    DeviceCreate,
    DeviceUpdate
)

router = APIRouter()

@router.get("/hello", response_model=HelloWorldResponse)
async def hello_world():
    """Simple hello world endpoint"""
    return HelloWorldResponse(
        message="Hello World from FastAPI!",
        timestamp=datetime.now(),
        data={"source": "backend", "framework": "FastAPI"}
    )

@router.post("/echo", response_model=HelloWorldResponse)
async def echo_message(request: MessageRequest):
    """Echo back the message sent from frontend"""
    return HelloWorldResponse(
        message=f"Echo: {request.message}",
        timestamp=datetime.now(),
        data={
            "original_message": request.message,
            "user_id": request.user_id,
            "processed_by": "FastAPI backend"
        }
    )

# Test Cases endpoints
@router.get("/test-cases", response_model=List[TestCase])
async def get_test_cases(db: AsyncSession = Depends(get_db)):
    """Get all test cases"""
    result = await db.execute(select(TestCaseModel))
    test_cases = result.scalars().all()
    return test_cases

@router.post("/test-cases", response_model=TestCase)
async def create_test_case(test_case: TestCaseCreate, db: AsyncSession = Depends(get_db)):
    """Create a new test case"""
    db_test_case = TestCaseModel(**test_case.dict())
    db.add(db_test_case)
    await db.commit()
    await db.refresh(db_test_case)
    return db_test_case

@router.get("/test-cases/{test_case_id}", response_model=TestCase)
async def get_test_case(test_case_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific test case by ID"""
    result = await db.execute(select(TestCaseModel).where(TestCaseModel.id == test_case_id))
    test_case = result.scalar_one_or_none()
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    return test_case

# Devices endpoints
@router.get("/devices", response_model=List[Device])
async def get_devices(db: AsyncSession = Depends(get_db)):
    """Get all devices"""
    result = await db.execute(select(DeviceModel))
    devices = result.scalars().all()
    return devices

@router.post("/devices", response_model=Device)
async def create_device(device: DeviceCreate, db: AsyncSession = Depends(get_db)):
    """Create a new device"""
    db_device = DeviceModel(**device.dict())
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device

@router.get("/devices/{device_id}", response_model=Device)
async def get_device(device_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific device by ID"""
    result = await db.execute(select(DeviceModel).where(DeviceModel.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device
