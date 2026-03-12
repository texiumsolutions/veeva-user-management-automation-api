#!/bin/bash

echo "Starting Texium FastAPI server..."

# Go to project root Azure uses
cd /home/site/wwwroot || exit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Moving to app directory..."
cd backend/app || exit

echo "Starting FastAPI..."
uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}