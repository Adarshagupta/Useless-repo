#!/bin/bash

# Start PostgreSQL using Docker
echo "Starting PostgreSQL..."
cd backend
docker-compose up -d
cd ..

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
sleep 5

# Run database migrations
echo "Running database migrations..."
cd backend
alembic upgrade head

# Initialize the database with sample data
echo "Initializing the database with sample data..."
python -m app.initial_data

# Start the backend server
echo "Starting the backend server..."
python run.py &
BACKEND_PID=$!
cd ..

# Wait for the backend to start
echo "Waiting for the backend to start..."
sleep 5

# Start the frontend
echo "Starting the frontend..."
npm run dev

# When the frontend is stopped, also stop the backend
kill $BACKEND_PID

echo "All processes stopped."
