# Self-Hosted AI Starter Kit

The **Self-Hosted AI Starter Kit** is a Docker Compose template designed to quickly bootstrap a fully featured local AI and low-code development environment. This setup includes essential services such as N8N for workflow automation, PostgreSQL for data storage, Ollama for local LLMs, Qdrant for vector storage, and more.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Services Overview](#services-overview)
- [Usage](#usage)
- [Scripts](#scripts)
- [Upgrading](#upgrading)
- [Support](#support)

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- Basic knowledge of Docker and command-line usage.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tazomatalax/Self-Hosted-AI-Starter-Kit.git
   cd self-hosted-ai-starter-kit
   ```

2. **Create a `.env` File**:
   Create a `.env` file in the root directory and define the following variables:
   ```env
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_postgres_db
   N8N_ENCRYPTION_KEY=your_encryption_key
   N8N_USER_MANAGEMENT_JWT_SECRET=your_jwt_secret
   ```

3. **Start the Services**:
   If you are using a nvidia GPU, run the following command to start all services:
   ```bash
   ./run.sh
   ```

   If you plan to use your PC's CPU, you will need to edit the run, stop, and update scripts to reflect that. Just uncomment the CPU profile commands and comment the GPU profile commands.

## Services Overview

### 1. N8N
- **Image**: `n8nio/n8n:latest`
- **Ports**: `5678:5678`
- **Description**: A low-code platform for automating workflows.

### 2. PostgreSQL
- **Image**: `postgres:16-alpine`
- **Ports**: `5432:5432`
- **Description**: Database service for storing N8N data.

### 3. Ollama
- **Image**: `ollama/ollama:latest`
- **Ports**: `11434:11434`
- **Description**: A platform for running local LLMs.

### 4. Qdrant
- **Image**: `qdrant/qdrant`
- **Ports**: `6333:6333`
- **Description**: High-performance vector storage.

### 5. Portainer
- **Image**: `portainer/portainer-ce`
- **Ports**: `9000:9000`
- **Description**: Management interface for Docker containers.

### 6. Homepage
- **Image**: `ghcr.io/gethomepage/homepage:latest`
- **Ports**: `3333:3000`
- **Description**: A customizable homepage for quick access to services.

## Usage

- Access N8N at [http://localhost:5678](http://localhost:5678)
- Access PostgreSQL at [http://localhost:5432](http://localhost:5432)
- Access Ollama at [http://localhost:11434](http://localhost:11434)
- Access Qdrant at [http://localhost:6333](http://localhost:6333)
- Access Portainer at [http://localhost:9000](http://localhost:9000)
- Access Homepage at [http://localhost:3333](http://localhost:3333)

## Scripts

### `run.sh`
This script starts the Docker containers using the GPU profile:
```bash
#!/bin/bash

# Run docker-compose with the GPU profile
docker compose --profile gpu-nvidia up

# Run docker-compose with the CPU profile
# docker compose --profile cpu up

# Display the host IP and Homer URL
echo "Docker containers have been started."
echo "Access your services at: http://localhost:3333 (Homepage URL)"
```

### `update.sh`
This script updates the Docker containers:
```bash
#!/bin/bash


# Pull the latest images and recreate the containers with the GPU profile
docker compose --profile gpu-nvidia pull
docker compose create && docker compose --profile gpu-nvidia up -d

# Pull the latest images and recreate the containers with the CPU profile
# docker compose --profile cpu pull
# docker compose create && docker compose --profile cpu up

# Display the host IP and Homer URL
echo "Docker containers have been updated."
echo "Access your services at: http://localhost:3333 (Homepage URL)"
```

### `stop.sh`
This script stops all running containers:
```bash
#!/bin/bash

docker compose --profile gpu-nvidia down

# docker compose --profile cpu down
```



## Upgrading Containers

To upgrade your services, run the following commands:
```bash
./update.sh
```

## Support

For issues or questions, please open an issue in the repository or join the community discussions.

---

This README provides a concise overview of setting up and using the self-hosted AI starter kit. Follow the instructions carefully to ensure a smooth installation and operation of the services.
