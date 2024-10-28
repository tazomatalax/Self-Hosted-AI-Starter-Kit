#!/bin/bash

# Wait for Portainer to be ready
echo "Waiting for Portainer to start..."
until $(curl --output /dev/null --silent --head --fail http://localhost:9000/api/status); do
    printf '.'
    sleep 5
done

echo "Portainer is ready!"

# Initialize Portainer admin user
curl -X POST "http://localhost:9000/api/users/admin/init" \
    -H "Content-Type: application/json" \
    -d '{
        "Username": "admin",
        "Password": "Asailorwent2ccc!"
    }'

echo "Portainer admin user created!"
