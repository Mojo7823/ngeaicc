#!/bin/bash

echo "🛑 Stopping AI Testing Standard Platform..."

# Stop Docker containers
echo "🐘 Stopping PostgreSQL..."
docker compose down

# Kill any running uvicorn processes
echo "🔧 Stopping FastAPI backend..."
pkill -f "uvicorn app.main:app" || true

# Kill any running npm dev processes
echo "🎨 Stopping Vue.js frontend..."
pkill -f "npm run dev" || true
pkill -f "vite" || true

echo "✅ All services stopped!"
