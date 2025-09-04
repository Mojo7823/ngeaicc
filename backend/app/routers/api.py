from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List, Optional

from app.database import get_db, TestCase as TestCaseModel, Device as DeviceModel, TOEDescription as TOEDescriptionModel
from app.models.schemas import (
    HelloWorldResponse, 
    MessageRequest,
    TestCase, 
    TestCaseCreate, 
    TestCaseUpdate,
    Device,
    DeviceCreate,
    DeviceUpdate,
    TOEDescription,
    TOEDescriptionCreate,
    TOEDescriptionUpdate
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

# TOE Description endpoints
@router.get("/toe-description", response_model=Optional[TOEDescription])
async def get_toe_description(db: AsyncSession = Depends(get_db)):
    """Get the current TOE description (latest one)"""
    result = await db.execute(
        select(TOEDescriptionModel).order_by(TOEDescriptionModel.updated_at.desc())
    )
    toe_description = result.scalar_one_or_none()
    return toe_description

@router.post("/toe-description", response_model=TOEDescription)
async def create_toe_description(toe_description: TOEDescriptionCreate, db: AsyncSession = Depends(get_db)):
    """Create a new TOE description"""
    db_toe_description = TOEDescriptionModel(**toe_description.dict())
    db.add(db_toe_description)
    await db.commit()
    await db.refresh(db_toe_description)
    return db_toe_description

@router.put("/toe-description/{toe_description_id}", response_model=TOEDescription)
async def update_toe_description(
    toe_description_id: str, 
    toe_description: TOEDescriptionUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Update an existing TOE description"""
    result = await db.execute(
        select(TOEDescriptionModel).where(TOEDescriptionModel.id == toe_description_id)
    )
    db_toe_description = result.scalar_one_or_none()
    if not db_toe_description:
        raise HTTPException(status_code=404, detail="TOE Description not found")
    
    # Update fields
    update_data = toe_description.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_toe_description, field, value)
    
    await db.commit()
    await db.refresh(db_toe_description)
    return db_toe_description

@router.get("/toe-description/{toe_description_id}", response_model=TOEDescription)
async def get_toe_description_by_id(toe_description_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific TOE description by ID"""
    result = await db.execute(
        select(TOEDescriptionModel).where(TOEDescriptionModel.id == toe_description_id)
    )
    toe_description = result.scalar_one_or_none()
    if not toe_description:
        raise HTTPException(status_code=404, detail="TOE Description not found")
    return toe_description
