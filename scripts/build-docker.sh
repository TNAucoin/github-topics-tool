#!/bin/bash
# Build and tag the GitHub Topics Tool Docker image

echo "Building GitHub Topics Tool Docker image..."
docker build -f docker/Dockerfile -t github-topics:latest .

echo "Creating versioned tag..."
VERSION=$(date +%Y%m%d)
docker tag github-topics:latest github-topics:$VERSION

echo ""
echo "Build complete! Images created:"
echo "  - github-topics:latest"
echo "  - github-topics:$VERSION"
echo ""
echo "To push to Docker Hub (optional):"
echo "  docker tag github-topics:latest yourusername/github-topics:latest"
echo "  docker push yourusername/github-topics:latest"