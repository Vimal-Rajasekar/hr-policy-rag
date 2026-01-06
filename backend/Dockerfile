FROM python:3.11-slim

WORKDIR /app

# Copy entire backend folder
COPY . /app/backend

# Make backend importable
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
