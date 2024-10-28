#!/bin/bash

docker compose --profile gpu-nvidia pull
docker compose create && docker compose --profile gpu-nvidia up -d

# Display the host IP and Homer URL
echo "Docker containers have been updated."
echo "Access your services at: http://localhost:3333 (Homepage URL)"