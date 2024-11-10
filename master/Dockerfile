# Use the Debian Slim base image
FROM docker.io/debian:stable-slim

# Install dependencies for Python, Scapy, and networking tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tcpdump \
    libpcap-dev \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory inside the container
WORKDIR /app

# Copy all files from the current directory (including requirements.txt)
COPY . /app/

# Create and activate a virtual environment
RUN python3 -m venv /app/venv

# Install Python dependencies from requirements.txt inside the virtual environment
RUN /app/venv/bin/pip install -r /app/requirements.txt

# Create the logs directory for packet logs (if not already created by the script)
RUN mkdir -p /app/logs

# Set the virtual environment path for running the Python script
CMD ["/app/venv/bin/python", "/app/monitor.py"]
