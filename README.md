# GitHub Topics Tool

A command-line tool to manage GitHub repository topics in bulk. Add, update, or replace topics across multiple repositories with ease.

## Project Structure

```
github-topics-tool/
├── README.md                     # Main documentation
├── Makefile                     # Build and run commands
├── pyproject.toml               # Python project configuration
├── uv.lock                      # Dependency lock file
├── github-topics.yml            # Sample configuration file
├── src/                         # Source code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main entry point
│   ├── cli.py                   # Command line interface
│   ├── config.py                # Configuration management
│   └── topics.py                # GitHub Topics API logic
├── scripts/                     # Executable scripts
│   ├── build-docker.sh         # Docker build script
│   └── github-topics.sh        # Main wrapper script
├── docker/                      # Docker configuration
│   ├── Dockerfile              # Docker image definition
│   └── docker-compose.yml      # Docker Compose configuration
└── docs/                        # Documentation
    └── DOCKER-SETUP.md         # Docker setup guide
```

## Features

- ✅ Bulk topic management across multiple repositories
- ✅ Global owner support - set once, use for all repos
- ✅ Global topics - automatically add common topics to all repos
- ✅ Flexible input methods (CLI args, config file, file list)
- ✅ Dry-run mode for testing
- ✅ Replace or append topic modes
- ✅ Progress tracking for large batches
- ✅ Docker support - no Python installation required

## Quick Start

### Prerequisites

See [docs/DOCKER-SETUP.md](https://github.com/TNAucoin/github-topics-tool/blob/main/docs/DOCKER-SETUP.md) for Docker-specific setup.

**REQUIRED**: Set your GitHub token in one of these ways:

**Option A: Environment variable**
```bash
export GITHUB_TOKEN=ghp_YourGitHubTokenHere
```

**Option B: .env file (recommended for development)**
```bash
# Create a .env file in the project root
echo "GITHUB_TOKEN=ghp_YourGitHubTokenHere" > .env
```

### Option 1: Using Make (Recommended)

```bash
# Clone the repository
git clone https://github.com/TNAucoin/github-topics-tool.git
cd github-topics-tool

# Complete setup (builds Docker image and generates config)
make dev-setup

# Edit github-topics.yml with your settings

# Run the tool (GITHUB_TOKEN must be set)
make run

# Or run in dry-run mode first
make run-dry
```

### Option 2: Docker (Manual)

```bash
# Build the Docker image
./scripts/build-docker.sh

# Generate initial config file
./scripts/github-topics.sh --init

# Edit the generated github-topics.yml with your settings

# Run the tool (GITHUB_TOKEN must be set)
./scripts/github-topics.sh
```

### Option 3: Python Installation

```bash
# Clone the repository
git clone https://github.com/TNAucoin/github-topics-tool.git
cd github-topics-tool

# Generate initial config file
uv run src/main.py --init

# Edit github-topics.yml with your settings
# Run the tool
uv run src/main.py
```

## Configuration

### Sample `github-topics.yml`

```yaml
# GITHUB_TOKEN environment variable must be set separately
global_owner: YourOrgName  # Default owner for all repos
repositories:
  - repo: repo1  # Uses global_owner
  - repo: repo2  # Uses global_owner
  - owner: different-org  # Override global_owner
    repo: special-repo
    topics: [custom, special]
global_topics:
  - managed
  - automated
settings:
  replace_existing: false  # Append topics (true = replace all)
  dry_run: false          # Test mode
```

### Sample `repos.txt` file

```
# List of repositories, one per line
# Lines starting with # are ignored
owner/repo1
owner/repo2
different-org/special-repo
myorg/project-alpha
myorg/project-beta
```

Use with: `./scripts/github-topics.sh --repos-file repos.txt --topics python automation`

**Note**: By default, topics are added to existing repository topics. Use `--replace` to replace all existing topics instead.

## Usage Examples

### Using Config File

**With Make (recommended - hides sensitive tokens):**
```bash
# Use default config file (github-topics.yml)
make run

# Use custom config file
make run-config CONFIG=my-config.yml

# Dry-run mode
make run-dry
```

**Manual approach:**
```bash
# Use default config file (github-topics.yml)
./scripts/github-topics.sh

# Use custom config
./scripts/github-topics.sh --config my-config.yml
```

### Docker Examples
```bash
# With config file
docker run --rm -it -v $(pwd):/workspace -e GITHUB_TOKEN=$GITHUB_TOKEN github-topics:latest

# Command line arguments
docker run --rm -it -v $(pwd):/workspace -e GITHUB_TOKEN=$GITHUB_TOKEN github-topics:latest \
  --repo owner/repo --topics docker kubernetes

# Using docker-compose (from docker/ directory)
cd docker && docker-compose run --rm github-topics

# Using the wrapper script (easiest)
./scripts/github-topics.sh --repo owner/repo --topics automated

# Windows PowerShell
docker run --rm -it -v ${PWD}:/workspace -e GITHUB_TOKEN=$env:GITHUB_TOKEN github-topics:latest
```

### Command Line Mode
```bash
# Single repository
./github-topics --repo owner/repo --topics python cli tool

# Multiple repositories
./github-topics --repos owner/repo1 owner/repo2 --topics docker kubernetes

# From file list
./github-topics --repos-file repos.txt --topics automated

# Replace mode (removes existing topics)
./github-topics --repo owner/repo --topics new topic --replace

# Dry run (preview changes)
./github-topics --repo owner/repo --topics test --dry-run
```

### Using Environment Variables
```bash
# Method 1: Export environment variable
export GITHUB_TOKEN=ghp_YourTokenHere
./scripts/github-topics.sh --repo owner/repo --topics cli

# Method 2: Create .env file (automatically loaded)
echo "GITHUB_TOKEN=ghp_YourTokenHere" > .env
./scripts/github-topics.sh --repo owner/repo --topics cli
```

## Requirements

- GitHub personal access token with `repo` scope (set as `GITHUB_TOKEN` environment variable or in `.env` file)
- One of:
  - Docker (recommended)
  - Python 3.13+ with uv
  - Make


**Security Note**: GitHub tokens are never stored in config files - they must be set as environment variables or in a `.env` file (which is gitignored for security).

## Development

### Code Quality
This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting (configured for tab indentation):

```bash
# Install development dependencies
make install-dev

# Run linter
make lint

# Auto-fix linting issues
make lint-fix

# Format code
make format

# Check formatting
make format-check

# Run all checks
make check-all
```

