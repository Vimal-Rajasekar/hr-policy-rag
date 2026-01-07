FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy everything inside backend/
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start FastAPI using Render's injected PORT
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
