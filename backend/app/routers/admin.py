from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, func, delete
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio

from app.database import get_db, TestCase as TestCaseModel, Device as DeviceModel, TOEDescription as TOEDescriptionModel
from app.models.schemas import AdminStats, DatabaseTable, DatabaseHealth, ApiEndpoint, SystemInfo

router = APIRouter()

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get comprehensive system and database statistics"""
    
    # Get database statistics
    test_cases_count = await db.scalar(select(func.count(TestCaseModel.id)))
    devices_count = await db.scalar(select(func.count(DeviceModel.id)))
    toe_descriptions_count = await db.scalar(select(func.count(TOEDescriptionModel.id)))
    
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
            "total_tables": 3,
            "test_cases_count": test_cases_count or 0,
            "devices_count": devices_count or 0,
            "toe_descriptions_count": toe_descriptions_count or 0,
            "recent_activity": {
                "test_cases_last_24h": recent_test_cases or 0
            }
        },
        "api": {
            "endpoints_available": 20,
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

# Database CRUD operations for admin management
@router.get("/database/data/{table_name}")
async def get_table_data(table_name: str, db: AsyncSession = Depends(get_db)):
    """Get data from a specific table"""
    
    if table_name not in ['test_cases', 'devices', 'toe_descriptions']:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    try:
        if table_name == 'test_cases':
            result = await db.execute(select(TestCaseModel))
            data = result.scalars().all()
        elif table_name == 'devices':
            result = await db.execute(select(DeviceModel))
            data = result.scalars().all()
        elif table_name == 'toe_descriptions':
            result = await db.execute(select(TOEDescriptionModel))
            data = result.scalars().all()
        
        # Convert to dict for JSON serialization
        return [
            {
                **{column.name: getattr(item, column.name) for column in item.__table__.columns}
            }
            for item in data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@router.delete("/database/data/{table_name}/{item_id}")
async def delete_table_item(table_name: str, item_id: str, db: AsyncSession = Depends(get_db)):
    """Delete an item from a specific table"""
    
    if table_name not in ['test_cases', 'devices', 'toe_descriptions']:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    try:
        if table_name == 'test_cases':
            result = await db.execute(select(TestCaseModel).where(TestCaseModel.id == item_id))
            item = result.scalar_one_or_none()
            if item:
                await db.delete(item)
        elif table_name == 'devices':
            result = await db.execute(select(DeviceModel).where(DeviceModel.id == item_id))
            item = result.scalar_one_or_none()
            if item:
                await db.delete(item)
        elif table_name == 'toe_descriptions':
            result = await db.execute(select(TOEDescriptionModel).where(TOEDescriptionModel.id == item_id))
            item = result.scalar_one_or_none()
            if item:
                await db.delete(item)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        await db.commit()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")

@router.post("/database/execute-sql")
async def execute_sql_query(query_data: dict, db: AsyncSession = Depends(get_db)):
    """Execute a custom SQL query (READ ONLY)"""
    
    query = query_data.get("query", "").strip().lower()
    
    # Security check - only allow SELECT queries
    if not query.startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
    
    # Additional security - block potentially dangerous keywords
    dangerous_keywords = ['drop', 'delete', 'update', 'insert', 'alter', 'create', 'truncate']
    if any(keyword in query for keyword in dangerous_keywords):
        raise HTTPException(status_code=400, detail="Query contains forbidden keywords")
    
    try:
        result = await db.execute(text(query_data["query"]))
        
        # Get column names
        columns = list(result.keys()) if result.keys() else []
        
        # Get data
        rows = []
        for row in result:
            rows.append(dict(row._mapping))
        
        return {
            "columns": columns,
            "rows": rows,
            "count": len(rows)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution error: {str(e)}")

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
        {"path": "/api/v1/toe-description", "method": "GET", "description": "Get TOE description", "category": "data"},
        {"path": "/api/v1/toe-description", "method": "POST", "description": "Create TOE description", "category": "data"},
        {"path": "/api/v1/toe-description/{id}", "method": "PUT", "description": "Update TOE description", "category": "data"},
        {"path": "/api/v1/toe-description/{id}", "method": "GET", "description": "Get specific TOE description", "category": "data"},
        {"path": "/api/v1/admin/stats", "method": "GET", "description": "System statistics", "category": "admin"},
        {"path": "/api/v1/admin/database/tables", "method": "GET", "description": "Database tables info", "category": "admin"},
        {"path": "/api/v1/admin/database/health", "method": "GET", "description": "Database health check", "category": "admin"},
        {"path": "/api/v1/admin/database/data/{table}", "method": "GET", "description": "Get table data", "category": "admin"},
        {"path": "/api/v1/admin/database/data/{table}/{id}", "method": "DELETE", "description": "Delete table item", "category": "admin"},
        {"path": "/api/v1/admin/database/execute-sql", "method": "POST", "description": "Execute SQL query", "category": "admin"},
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