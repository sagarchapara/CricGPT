#!/bin/bash

# Load Docker images
echo "Loading client_x86 Docker image..."
docker load < out/client_x86.tar.gz

echo "Loading server_x86 Docker image..."
docker load < out/server_x86.tar.gz

# Start Docker containers using docker-compose
echo "Starting Docker containers with docker-compose..."
docker-compose up -d

# List all Docker containers
echo "Listing all Docker containers..."
docker ps --all