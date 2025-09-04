from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
import uuid
import subprocess
import json
from typing import Dict, Optional

router = APIRouter()

# In-memory storage for ping sessions (in production, use Redis or database)
ping_sessions: Dict[str, Dict] = {}

class PingStartRequest(BaseModel):
    ip_address: str
    packet_size: Optional[int] = 64
    additional_command: Optional[str] = ""

class PingStopRequest(BaseModel):
    session_id: str

class PingStartResponse(BaseModel):
    session_id: str
    status: str
    message: str

class PingStopResponse(BaseModel):
    status: str
    message: str

async def run_ping_process(session_id: str, ip_address: str, packet_size: int, additional_command: str):
    """Run ping process in background"""
    try:
        # Build ping command
        cmd = ["ping"]
        
        # Add packet size parameter
        cmd.extend(["-s", str(packet_size)])
        
        # Add additional command parameters if provided
        if additional_command.strip():
            # Simple parsing - in production, use proper command parsing
            cmd.extend(additional_command.split())
        
        # Add target IP
        cmd.append(ip_address)
        
        # Update session status
        ping_sessions[session_id]["status"] = "running"
        ping_sessions[session_id]["command"] = " ".join(cmd)
        
        # Start process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        ping_sessions[session_id]["process"] = process
        
        # Read output line by line
        while process.poll() is None and ping_sessions[session_id]["status"] == "running":
            line = process.stdout.readline()
            if line:
                ping_sessions[session_id]["output"].append(line.strip())
            await asyncio.sleep(0.1)
        
        # Process has ended
        ping_sessions[session_id]["status"] = "stopped"
        
    except Exception as e:
        ping_sessions[session_id]["status"] = "error"
        ping_sessions[session_id]["error"] = str(e)

@router.post("/ping/start", response_model=PingStartResponse)
async def start_ping(request: PingStartRequest, background_tasks: BackgroundTasks):
    """Start a ping test"""
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Initialize session
        ping_sessions[session_id] = {
            "ip_address": request.ip_address,
            "packet_size": request.packet_size,
            "additional_command": request.additional_command,
            "status": "starting",
            "output": [],
            "created_at": asyncio.get_event_loop().time()
        }
        
        # Start ping process in background
        background_tasks.add_task(
            run_ping_process,
            session_id,
            request.ip_address,
            request.packet_size,
            request.additional_command or ""
        )
        
        return PingStartResponse(
            session_id=session_id,
            status="started",
            message=f"Ping test started for {request.ip_address}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start ping: {str(e)}")

@router.post("/ping/stop", response_model=PingStopResponse)
async def stop_ping(request: PingStopRequest):
    """Stop a ping test"""
    try:
        if request.session_id not in ping_sessions:
            raise HTTPException(status_code=404, detail="Ping session not found")
        
        session = ping_sessions[request.session_id]
        
        # Stop the process if it's running
        if "process" in session and session["process"].poll() is None:
            session["process"].terminate()
            await asyncio.sleep(0.1)
            if session["process"].poll() is None:
                session["process"].kill()
        
        # Update session status
        session["status"] = "stopped"
        
        return PingStopResponse(
            status="stopped",
            message="Ping test stopped successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop ping: {str(e)}")

@router.get("/ping/status/{session_id}")
async def get_ping_status(session_id: str):
    """Get ping test status and output"""
    try:
        if session_id not in ping_sessions:
            raise HTTPException(status_code=404, detail="Ping session not found")
        
        session = ping_sessions[session_id]
        
        return {
            "session_id": session_id,
            "status": session["status"],
            "ip_address": session["ip_address"],
            "packet_size": session["packet_size"],
            "output": session["output"],
            "command": session.get("command", ""),
            "error": session.get("error", None),
            "created_at": session["created_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get ping status: {str(e)}")

@router.get("/ping/sessions")
async def list_ping_sessions():
    """List all ping sessions"""
    try:
        sessions = []
        for session_id, session in ping_sessions.items():
            sessions.append({
                "session_id": session_id,
                "ip_address": session["ip_address"],
                "status": session["status"],
                "created_at": session["created_at"],
                "output_lines": len(session["output"])
            })
        
        return {"sessions": sessions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list sessions: {str(e)}")

@router.delete("/ping/session/{session_id}")
async def delete_ping_session(session_id: str):
    """Delete a ping session"""
    try:
        if session_id not in ping_sessions:
            raise HTTPException(status_code=404, detail="Ping session not found")
        
        # Stop process if running
        session = ping_sessions[session_id]
        if "process" in session and session["process"].poll() is None:
            session["process"].terminate()
        
        # Delete session
        del ping_sessions[session_id]
        
        return {"message": "Ping session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")