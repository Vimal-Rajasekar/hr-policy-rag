FROM python:3.11-slim

WORKDIR /app

# System deps (optional but safe)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
