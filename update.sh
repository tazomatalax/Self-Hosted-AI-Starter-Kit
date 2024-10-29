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