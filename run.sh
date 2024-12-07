#!/bin/bash

# Check for the -d flag
DETACH=""

if [[ "$1" == "-d" ]]; then
  DETACH="-d"
fi

# Run docker-compose with the GPU profile
docker compose --profile gpu-nvidia up $DETACH

# Run docker-compose with the CPU profile
# docker compose --profile cpu up $DETACH

# Display the host IP and Homer URL
echo "Docker containers have been started."
echo "Access your services at: http://localhost:3333 (Homepage URL)"
