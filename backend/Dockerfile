FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy source
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "microrush.api.app:app", "--host", "0.0.0.0", "--port", "8000"]