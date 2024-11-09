# master/Dockerfile
FROM debian:bullseye-slim

# Install dependencies for Python and Scapy
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tcpdump \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy the fuzzing script
COPY fuzzing_script.py /app/

# Create logs directory for packet logs
RUN mkdir -p /app/logs

# Run the fuzzing script by default
CMD ["python3", "/app/fuzzing_script.py"]
