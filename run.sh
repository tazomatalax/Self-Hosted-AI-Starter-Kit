#!/bin/bash

# Automatically export the host IP
export HOST_IP=$(hostname -I | awk '{print $1}')

# Create a .env file with the HOST_IP
echo "HOST_IP=$HOST_IP" > .env

# Run docker-compose
docker compose --profile gpu-nvidia up -d

# Display the host IP and Homer URL
echo "Docker containers have been started."
echo "Access your services at: http://$HOST_IP:8080 (Homer URL)"