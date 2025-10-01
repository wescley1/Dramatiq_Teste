FROM python:3.12-slim

# Install minimal build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install runtime deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Default command is to show help; services override the command
CMD ["python", "-c", "print('Container ready')"]
