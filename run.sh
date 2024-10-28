#!/bin/bash



# Run docker-compose
docker compose --profile gpu-nvidia up -d

# Display the host IP and Homer URL
echo "Docker containers have been started."
echo "Access your services at: http://localhost:8080 (Homer URL)"
