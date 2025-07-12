# Docker Setup Guide

This guide covers Docker-specific setup for the GitHub Topics Tool. For general usage and configuration, see the [main README](https://github.com/TNAucoin/github-topics-tool/blob/main/README.md).

## Prerequisites
- Docker Desktop: https://www.docker.com/products/docker-desktop/
- Git for cloning the repository

## Docker Setup

### Build the Image
```bash
git clone https://github.com/TNAucoin/github-topics-tool.git
cd github-topics-tool
./scripts/build-docker.sh
```

### Using the Docker Wrapper Script
```bash
# Set your token (see main README for .env file option)
export GITHUB_TOKEN=ghp_YourGitHubTokenHere

# Generate config and run
./scripts/github-topics.sh --init
./scripts/github-topics.sh
```

## Direct Docker Commands

### Basic Usage
```bash
# With config file in current directory
docker run --rm -it \
  -v $(pwd):/workspace \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  github-topics:latest

# With command line arguments
docker run --rm -it \
  -v $(pwd):/workspace \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  github-topics:latest \
  --repo owner/repo --topics docker automated
```

### Platform-Specific Commands

**Windows PowerShell:**
```powershell
docker run --rm -it `
  -v ${PWD}:/workspace `
  -e GITHUB_TOKEN=$env:GITHUB_TOKEN `
  github-topics:latest
```

**Windows Command Prompt:**
```cmd
docker run --rm -it -v %cd%:/workspace -e GITHUB_TOKEN=%GITHUB_TOKEN% github-topics:latest
```

## Docker Compose

From the `docker/` directory:
```bash
cd docker
docker-compose run --rm github-topics
docker-compose run --rm github-topics --repo owner/repo --topics test
```

## Docker-Specific Troubleshooting

### "Image not found"
```bash
./scripts/build-docker.sh
```

### File mounting issues
- Config files must be in your current working directory
- The Docker container mounts your current directory to `/workspace`
- Ensure you're running Docker commands from the project root

### Environment variables in Docker
- Use `-e GITHUB_TOKEN=$GITHUB_TOKEN` to pass environment variables
- .env files in your host directory are automatically loaded by the application

## Distribution to Team

1. Share the GitHub repository URL
2. Ensure team has Docker Desktop installed
3. Provide organization-specific config guidance