#!/bin/bash

# Navigate to the parent directory to run the module
cd "$(dirname "$0")/.."

# Install dependencies if needed (optional check)
# pip install -r microservice/requirements.txt

# Run the FastAPI app
uvicorn microservice.main:app --reload --host 0.0.0.0 --port 8000
