from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, func
from datetime import datetime
from typing import Dict, Any, List
import asyncio

from app.database import get_db, TestCase as TestCaseModel, Device as DeviceModel
from app.models.schemas import AdminStats, DatabaseTable, DatabaseHealth, ApiEndpoint, SystemInfo

router = APIRouter()

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get comprehensive system and database statistics"""
    
    # Get database statistics
    test_cases_count = await db.scalar(select(func.count(TestCaseModel.id)))
    devices_count = await db.scalar(select(func.count(DeviceModel.id)))
    
    # Get recent activity (last 24 hours)
    recent_test_cases = await db.scalar(
        select(func.count(TestCaseModel.id))
        .where(TestCaseModel.created_at >= func.now() - text("INTERVAL '24 hours'"))
    )
    
    # Get database size and table info
    db_size_result = await db.execute(text("""
        SELECT pg_size_pretty(pg_database_size(current_database())) as db_size
    """))
    db_size = db_size_result.scalar()
    
    return {
        "system": {
            "timestamp": datetime.now(),
            "status": "healthy",
            "database_size": db_size
        },
        "database": {
            "total_tables": 2,
            "test_cases_count": test_cases_count or 0,
            "devices_count": devices_count or 0,
            "recent_activity": {
                "test_cases_last_24h": recent_test_cases or 0
            }
        },
        "api": {
            "endpoints_available": 12,
            "status": "active"
        }
    }

@router.get("/database/tables", response_model=List[DatabaseTable])
async def get_database_tables(db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get information about all database tables"""
    
    # Get table information from PostgreSQL system catalogs
    result = await db.execute(text("""
        SELECT 
            schemaname,
            tablename,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
            pg_stat_get_numscans(c.oid) as scans,
            pg_stat_get_tuples_inserted(c.oid) as inserts,
            pg_stat_get_tuples_updated(c.oid) as updates,
            pg_stat_get_tuples_deleted(c.oid) as deletes
        FROM pg_tables pt
        LEFT JOIN pg_class c ON c.relname = pt.tablename
        WHERE schemaname = 'public'
        ORDER BY tablename
    """))
    
    tables = []
    for row in result:
        tables.append({
            "schema": row.schemaname,
            "name": row.tablename,
            "size": row.size,
            "statistics": {
                "scans": row.scans or 0,
                "inserts": row.inserts or 0,
                "updates": row.updates or 0,
                "deletes": row.deletes or 0
            }
        })
    
    return tables

@router.get("/database/health", response_model=DatabaseHealth)
async def get_database_health(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Check database health and connectivity"""
    
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        
        # Check pgvector extension
        pgvector_check = await db.execute(text("""
            SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector') as has_pgvector
        """))
        has_pgvector = pgvector_check.scalar()
        
        # Get database version
        version_result = await db.execute(text("SELECT version()"))
        db_version = version_result.scalar()
        
        return {
            "status": "healthy",
            "connection": "active",
            "pgvector_enabled": has_pgvector,
            "database_version": db_version,
            "last_check": datetime.now()
        }
    except Exception as e:
        return {
            "status": "error",
            "connection": "failed",
            "error": str(e),
            "last_check": datetime.now()
        }

@router.get("/api/endpoints", response_model=List[ApiEndpoint])
async def get_api_endpoints() -> List[Dict[str, Any]]:
    """Get list of all available API endpoints"""
    
    endpoints = [
        {"path": "/", "method": "GET", "description": "Root endpoint", "category": "system"},
        {"path": "/health", "method": "GET", "description": "Health check", "category": "system"},
        {"path": "/api/v1/hello", "method": "GET", "description": "Hello world", "category": "demo"},
        {"path": "/api/v1/echo", "method": "POST", "description": "Echo message", "category": "demo"},
        {"path": "/api/v1/test-cases", "method": "GET", "description": "Get all test cases", "category": "data"},
        {"path": "/api/v1/test-cases", "method": "POST", "description": "Create test case", "category": "data"},
        {"path": "/api/v1/test-cases/{id}", "method": "GET", "description": "Get specific test case", "category": "data"},
        {"path": "/api/v1/devices", "method": "GET", "description": "Get all devices", "category": "data"},
        {"path": "/api/v1/devices", "method": "POST", "description": "Create device", "category": "data"},
        {"path": "/api/v1/devices/{id}", "method": "GET", "description": "Get specific device", "category": "data"},
        {"path": "/api/v1/admin/stats", "method": "GET", "description": "System statistics", "category": "admin"},
        {"path": "/api/v1/admin/database/tables", "method": "GET", "description": "Database tables info", "category": "admin"},
        {"path": "/api/v1/admin/database/health", "method": "GET", "description": "Database health check", "category": "admin"},
        {"path": "/api/v1/admin/api/endpoints", "method": "GET", "description": "API endpoints list", "category": "admin"}
    ]
    
    return endpoints

@router.get("/system/info", response_model=SystemInfo)
async def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    
    return {
        "application": {
            "name": "AI Testing Standard Platform",
            "version": "1.0.0",
            "framework": "FastAPI",
            "python_version": "3.12+"
        },
        "database": {
            "type": "PostgreSQL",
            "version": "16+",
            "extensions": ["pgvector"]
        },
        "frontend": {
            "framework": "Vue.js 3",
            "build_tool": "Vite",
            "language": "TypeScript"
        },
        "deployment": {
            "containerization": "Docker",
            "orchestration": "Docker Compose"
        },
        "timestamp": datetime.now()
    }