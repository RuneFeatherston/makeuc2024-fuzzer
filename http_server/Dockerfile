# Start with a minimal base image that has a compiler
FROM debian:latest

# Update the package manager and install necessary packages
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the vulnerable HTTP server source code into the container
COPY vuln_http_server.c .

# Compile the C source code to create the server executable
RUN gcc -o vuln_http_server vuln_http_server.c

# Expose the server's port (e.g., 8080) to the Docker host
EXPOSE 8080

# Start the vulnerable HTTP server when the container runs
CMD ["./vuln_http_server"]
