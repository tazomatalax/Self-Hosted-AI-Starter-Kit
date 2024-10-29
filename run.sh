#!/bin/bash

# Run docker-compose with the GPU profile
docker compose --profile gpu-nvidia up

# Run docker-compose with the CPU profile
# docker compose --profile cpu up

# Display the host IP and Homer URL
echo "Docker containers have been started."
echo "Access your services at: http://localhost:3333 (Homepage URL)"
