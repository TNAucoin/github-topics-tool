FROM python:3.11-slim

WORKDIR /app

# Copy all source files into the image
COPY src/ .

# Install Python dependencies
RUN pip install --no-cache-dir pyyaml requests python-dotenv

# Create a wrapper script that handles config file mounting
RUN echo '#!/bin/sh\npython /app/main.py "$@"' > /usr/local/bin/github-topics && \
    chmod +x /usr/local/bin/github-topics

# Set working directory to /workspace for user files
WORKDIR /workspace

ENTRYPOINT ["github-topics"]