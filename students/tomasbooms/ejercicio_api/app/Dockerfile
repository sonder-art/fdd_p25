# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# Leverage Docker layer caching: install deps first
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Then copy the rest of your code
COPY . .

# Switch to non-root
USER appuser

# Expose port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

