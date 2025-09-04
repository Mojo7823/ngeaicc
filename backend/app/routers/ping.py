import asyncio
import subprocess
import uuid
import platform
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
import json

router = APIRouter(prefix="/ping")

# Store active ping sessions
active_sessions: Dict[str, Dict] = {}

class PingRequest(BaseModel):
    target: str
    packet_size: int = 32
    additional_args: str = ""

class PingResponse(BaseModel):
    sessionId: str

class StopPingRequest(BaseModel):
    session_id: str

@router.post("/start", response_model=PingResponse)
async def start_ping(request: PingRequest):
    """Start a ping session"""
    session_id = str(uuid.uuid4())
    
    # Validate the target
    if not request.target:
        raise HTTPException(status_code=400, detail="Target IP/hostname is required")
    
    # Build ping command based on platform
    system = platform.system().lower()
    if system == "windows":
        ping_cmd = ["ping", "-n", "4"]  # Windows ping
        if request.packet_size and request.packet_size != 32:
            ping_cmd.extend(["-l", str(request.packet_size)])
    else:
        ping_cmd = ["ping", "-c", "4"]  # Linux/Unix ping
        if request.packet_size and request.packet_size != 32:
            ping_cmd.extend(["-s", str(request.packet_size)])
    
    # Add additional arguments if provided
    if request.additional_args:
        # Split and add additional args (be careful with security)
        additional_args = request.additional_args.split()
        # Filter out potentially dangerous arguments
        safe_args = []
        for arg in additional_args:
            if system == "windows":
                if arg.startswith('-') and arg in ['-n', '-l', '-t', '-w']:
                    safe_args.append(arg)
                elif not arg.startswith('-'):
                    safe_args.append(arg)
            else:
                if arg.startswith('-') and arg in ['-c', '-i', '-t', '-W', '-w', '-q', '-v', '-s']:
                    safe_args.append(arg)
                elif not arg.startswith('-'):
                    safe_args.append(arg)
        ping_cmd.extend(safe_args)
    
    # Add target
    ping_cmd.append(request.target)
    
    # Store session info
    active_sessions[session_id] = {
        "command": ping_cmd,
        "process": None,
        "websockets": []
    }
    
    return PingResponse(sessionId=session_id)

@router.post("/stop")
async def stop_ping(request: StopPingRequest):
    """Stop a ping session"""
    session_id = request.session_id
    
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    
    # Stop the process if running
    if session["process"]:
        try:
            session["process"].terminate()
            await asyncio.sleep(0.1)
            if session["process"].returncode is None:
                session["process"].kill()
        except:
            pass
    
    # Close all websockets
    for ws in session["websockets"]:
        try:
            await ws.close()
        except:
            pass
    
    # Remove session
    del active_sessions[session_id]
    
    return {"message": "Ping session stopped"}

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for streaming ping output"""
    if session_id not in active_sessions:
        await websocket.close(code=4004, reason="Session not found")
        return
    
    await websocket.accept()
    session = active_sessions[session_id]
    session["websockets"].append(websocket)
    
    try:
        # Start the ping process
        process = await asyncio.create_subprocess_exec(
            *session["command"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            universal_newlines=True
        )
        
        session["process"] = process
        
        # Send initial message
        await websocket.send_text(json.dumps({
            "type": "output",
            "content": f"Starting ping: {' '.join(session['command'])}"
        }))
        
        # Stream output
        while True:
            line = await process.stdout.readline()
            if not line:
                break
                
            # Send output to websocket
            await websocket.send_text(json.dumps({
                "type": "output",
                "content": line.strip()
            }))
        
        # Wait for process to complete
        await process.wait()
        
        # Send completion message
        await websocket.send_text(json.dumps({
            "type": "finished",
            "content": f"Ping completed with exit code: {process.returncode}"
        }))
        
    except WebSocketDisconnect:
        # Client disconnected
        pass
    except Exception as e:
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "content": f"Error: {str(e)}"
            }))
        except:
            pass
    finally:
        # Cleanup
        if session["process"]:
            try:
                session["process"].terminate()
            except:
                pass
        
        # Remove websocket from session
        if websocket in session["websockets"]:
            session["websockets"].remove(websocket)
        
        try:
            await websocket.close()
        except:
            pass