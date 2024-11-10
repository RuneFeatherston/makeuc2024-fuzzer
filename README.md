# Bitstream Fuzzer

## Overview
This project is a bitstream-level fuzzer designed to identify vulnerabilities within network packets. By directly manipulating the raw bitstream of packets, it uncovers potential buffer overflows and memory corruption issues that high-level fuzzers might miss. The setup uses Docker for containerization, with Docker Compose to manage and orchestrate multiple containers.

## Prerequisites
- **Docker** and **Docker Compose** must be installed on your system. If you haven't installed them, you can download them here:
  - [Docker Installation Guide](https://docs.docker.com/get-docker/)
  - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

## Getting Started

### 1. Clone the Repository
First, clone the project repository to your local machine:

```bash
git clone https://github.com/RuneFeatherston/makeuc2024-fuzzer.git
cd bitstream-fuzzer
```

### 2. Build the Docker Containers
User `docker-compose build` to build all necessary images for the project:
```bash 
docker-compose build
```
This command will create images for each service defined in the `docker-compose.yml` file. Ensure all dependencies are installed during this step.

### 3. Run the Project
After building the images, start up the containers using `docker-compose up`:
```bash
docker-compose up
```
This command will initialize the containers, creating a virtual network for the fuzzer to operate on. You should see logs from each service in the terminal, showing packet mutations, crash attempts, and any error outputs.

### 4. Stopping the Containers.
To stop the containers, press `CTRL+C` in the terminal where the services are running. Alternatively, you can stop and remove all containers with:
```bash
docker-compose down
```

### Configuration and Customation
You can configure various parameters for the fuzzer in the `docker-compose.yml` file. To adjust mutation settings, logging directories, or network configruations, update these values directly in the file before running `docker-compose up` again.

### Project Structure
- **fuzzer/** - Contains the core fuzzer code and mutation functions
- **docker-compose.yml** - Docker Compose file that defines services, networks, and volumes
- **http_server/** - Directory with the code for the HTTP server and crash logging logic

### Troubleshooting
Sometimes, fuzzing can be constrained by the memory overwrite systems within the server hosting the HTTP server. You may need to investigate memory segmentation within the gcc compilation process to prevent the server from being spread across the container's memory-space.