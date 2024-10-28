#!/bin/bash

# Automatically export the host IP
export HOST_IP=$(hostname -I | awk '{print $1}')

# Run docker-compose
docker compose --profile gpu-nvidia up

