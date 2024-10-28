#!/bin/bash

docker compose --profile gpu-nvidia pull
docker compose create && docker compose --profile gpu-nvidia up -d