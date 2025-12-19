# Examples

This directory contains executable examples demonstrating unbihexium capabilities.

## Structure

| Directory | Description |
|-----------|-------------|
| [serving/](serving/) | FastAPI REST API for model serving |
| [notebooks/](notebooks/) | Jupyter notebooks with tutorials |
| [scripts/](scripts/) | Standalone Python scripts |

## Quick Start

### Running the API Server

```bash
# Install dependencies
pip install unbihexium[all] fastapi uvicorn

# Start the server
uvicorn examples.serving.api:app --host 0.0.0.0 --port 8000

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/info
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/info` | GET | Library information |
| `/detect/ships` | POST | Ship detection |
| `/detect/buildings` | POST | Building detection |
| `/index/ndvi` | POST | NDVI calculation |

## Navigation

[Home](../README.md) | [Documentation](../docs/index.md) | [Model Zoo](../docs/model_zoo/catalog.md)
