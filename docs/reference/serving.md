# Serving API Reference

This document describes the REST API for the unbihexium serving module.

## Overview

The serving API provides HTTP endpoints for model inference and pipeline execution.

## Quick Start

```bash
# Start the server
uvicorn unbihexium.serving.app:app --host 0.0.0.0 --port 8000

# Check health
curl http://localhost:8000/health
```

## Endpoints

### System

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |

### Discovery

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/capabilities` | GET | List capabilities |
| `/models` | GET | List available models |

### Inference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/infer/{model_id}` | POST | Generic inference |
| `/detect/{model_id}` | POST | Object detection |
| `/segment/{model_id}` | POST | Semantic segmentation |

## Request Examples

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "ready": true
}
```

### List Models

```bash
curl http://localhost:8000/models
```

Response:
```json
{
  "count": 3,
  "models": [
    {"model_id": "ship_detector_tiny", "task": "detection", "description": "Ship detection"},
    {"model_id": "building_detector_tiny", "task": "detection", "description": "Building detection"},
    {"model_id": "water_detector_tiny", "task": "segmentation", "description": "Water segmentation"}
  ]
}
```

### Run Detection

```bash
curl -X POST http://localhost:8000/detect/ship_detector_tiny \
  -H "Content-Type: application/json" \
  -d '{"image_data": [[[0.5, 0.5], [0.5, 0.5]]], "threshold": 0.5}'
```

## Security

- Maximum payload size: 10 MB
- Allowed content types: `application/json`, `multipart/form-data`
- Optional API key authentication via `X-API-Key` header

## Navigation

[API Reference](api.md) | [Home](../index.md) | [CLI Reference](cli.md)
