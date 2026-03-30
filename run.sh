#!/bin/bash

# Run Backend
echo "Starting Backend..."
cd backend
pip install -r requirements.txt
python app.py &
BACKEND_PID=$!

# Run Frontend
echo "Starting Frontend..."
cd ../frontend
npm install
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID