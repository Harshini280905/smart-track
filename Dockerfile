# ─────────────────────────────────────────────────────────────────
# SmartTrack — Dockerfile
# Builds a lightweight Python 3.11 container for the Flask backend
# ─────────────────────────────────────────────────────────────────

# Stage 1: Use official slim Python base image
FROM python:3.11-slim

# Set metadata labels
LABEL maintainer="mukunth"
LABEL app="smarttrack"
LABEL version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_DEBUG=false

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (leverages Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the full application source code
COPY . .

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser /app
USER appuser

# Expose the application port
EXPOSE 5000

# Health check — Docker will ping /health every 30s
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start the Flask application
CMD ["python", "app.py"]
