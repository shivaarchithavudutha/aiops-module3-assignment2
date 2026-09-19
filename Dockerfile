# Stage 1: Build stage
FROM python:3.10-slim AS builder

WORKDIR /install

# Install compile tools if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

# Install dependencies into /install prefix
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final minimal runtime stage
FROM python:3.10-slim

WORKDIR /app

# Copy only the compiled Python packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application code and model artifact
COPY app/main.py app/model.joblib /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
