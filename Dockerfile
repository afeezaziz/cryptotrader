FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    sqlite3 \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a volume directory for the database
RUN mkdir -p /data
VOLUME /data

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
ENV FLASK_DEBUG=false
ENV PYTHONUNBUFFERED=1
ENV DB_PATH=/data/trader.db
ENV MAX_RECORD_AGE_DAYS=30

# Expose the port the app runs on
EXPOSE 5000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Command to run the application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
