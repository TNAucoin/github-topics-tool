#!/bin/bash
# GitHub Topics Tool - Docker Wrapper
# This script runs the tool via Docker without requiring Python on the host

# Set the Docker image name
IMAGE_NAME="github-topics:latest"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Check if the image exists locally
if ! docker image inspect $IMAGE_NAME &> /dev/null 2>&1; then
    echo "Docker image not found. Please run ./build-docker.sh first to build the image."
    exit 1
fi

# Run the Docker container with proper volume mounts
docker run --rm -it \
    -v "$(pwd):/workspace" \
    -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
    $IMAGE_NAME "$@"