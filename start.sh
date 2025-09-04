#!/bin/bash

echo "🚀 Starting AI Testing Standard Platform Setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start PostgreSQL
echo "🐘 Starting PostgreSQL with pgvector..."
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
timeout=30
while ! docker exec ngeaicc_postgres pg_isready -U postgres > /dev/null 2>&1; do
    if [ $timeout -le 0 ]; then
        echo "❌ PostgreSQL failed to start within 30 seconds"
        exit 1
    fi
    echo "Waiting for PostgreSQL... ($timeout seconds remaining)"
    sleep 1
    timeout=$((timeout-1))
done

echo "✅ PostgreSQL is ready!"

# Start backend
echo "🔧 Starting FastAPI backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🚀 Starting FastAPI server..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Give backend time to start
sleep 5

# Test backend
echo "🧪 Testing FastAPI backend..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ FastAPI backend is running!"
else
    echo "❌ FastAPI backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

cd ../frontend

# Install frontend dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start frontend
echo "🎨 Starting Vue.js frontend..."
npm run dev &
FRONTEND_PID=$!

# Give frontend time to start
sleep 3

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📍 Access URLs:"
echo "   Frontend:     http://localhost:5173"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo "   PostgreSQL:   localhost:5432"
echo ""
echo "🛑 To stop all services:"
echo "   Press Ctrl+C, then run: docker-compose down"
echo ""
echo "📋 Backend PID: $BACKEND_PID"
echo "📋 Frontend PID: $FRONTEND_PID"

# Keep script running
wait
