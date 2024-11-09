# http_server/Dockerfile
FROM debian:bullseye-slim

# Install Python to run a simple HTTP server
RUN apt-get update && apt-get install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Start a simple HTTP server on port 80
CMD ["python3", "-m", "http.server", "80"]
