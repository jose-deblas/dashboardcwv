# Multi-stage Dockerfile for Core Web Vitals Dashboard
# Uses uv for fast Python dependency installation

# Stage 1: Build stage with uv
FROM python:3.13-slim AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies using uv
# Create a virtual environment and install dependencies
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install -r pyproject.toml

# Stage 2: Runtime stage
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs

# Expose Streamlit default port
EXPOSE 8501

# Default command (can be overridden in docker-compose)
CMD ["python", "-m", "streamlit", "run", "src/dashboard/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
