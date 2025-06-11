# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements (if not present, create it first)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
