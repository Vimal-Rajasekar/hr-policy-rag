FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy backend code
COPY backend /app/backend

# Make backend importable
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Start FastAPI using Render's injected PORT
CMD ["sh", "-c", "exec uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT"]
