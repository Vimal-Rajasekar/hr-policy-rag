FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only frontend code
COPY . /app

# Install frontend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for backend URL (optional, you can override on Render)
ENV BACKEND_URL=http://localhost:8000/chat

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
