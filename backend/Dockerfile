FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy backend folder into /app/backend
COPY . /app/backend

# Make /app importable so "backend.*" works
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Start FastAPI
CMD ["sh", "-c", "exec uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT"]
