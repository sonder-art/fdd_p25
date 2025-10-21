FROM python:3.12-slim


# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# Leverage Docker layer caching: install deps first
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Then copy the rest of your code
COPY . .

# Switch to non-root
USER appuser

# If you're running a web app, override as needed
CMD ["python", "main.py"]
