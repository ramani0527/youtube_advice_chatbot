#!/bin/bash
set -e

# Wait for Qdrant to be ready
echo "Waiting for Qdrant..."
until curl -s http://qdrant:6333/healthz > /dev/null; do
  sleep 2
done
echo "Qdrant is up!"

# Run ingestion
echo "Running ingestion script..."
python scripts/ingestion-script.py || echo "Ingestion failed or already done."

# Start FastAPI
echo "Starting FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000