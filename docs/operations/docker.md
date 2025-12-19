# Docker Operations

This document describes Docker usage for unbihexium.

## Building the Image

```bash
# Build production image
docker build -t unbihexium:latest .

# Build with specific tag
docker build -t unbihexium:1.0.0 .
```

## Running Containers

### CLI Mode

```bash
# Run CLI help
docker run unbihexium:latest unbihexium --help

# Run specific command
docker run unbihexium:latest unbihexium zoo list
```

### API Server Mode

```bash
# Run API server
docker run -p 8000:8000 unbihexium:latest \
  uvicorn unbihexium.serving.app:app --host 0.0.0.0 --port 8000

# With volume for model cache
docker run -p 8000:8000 \
  -v unbihexium-cache:/home/unbihexium/.cache/unbihexium \
  unbihexium:latest \
  uvicorn unbihexium.serving.app:app --host 0.0.0.0 --port 8000
```

## Docker Compose

```yaml
version: "3.9"
services:
  unbihexium-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - unbihexium-cache:/home/unbihexium/.cache
    command: uvicorn unbihexium.serving.app:app --host 0.0.0.0 --port 8000
```

## Security Notes

- Container runs as non-root user (`unbihexium`, UID 1000)
- No secrets in image; use environment variables or mounted secrets
- Health check included for orchestration

## Image Details

| Property | Value |
|----------|-------|
| Base Image | python:3.12-slim |
| User | unbihexium (non-root) |
| Working Dir | /home/unbihexium |
| Exposed Port | 8000 |

## Navigation

[Operations](../index.md) | [Home](../index.md) | [Serving API](../reference/serving.md)
