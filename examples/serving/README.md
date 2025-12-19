# Serving Module

FastAPI-based REST API for serving unbihexium models.

## Files

- `api.py` - Main FastAPI application

## Usage

```bash
# Install dependencies
pip install fastapi uvicorn python-multipart

# Run server
uvicorn examples.serving.api:app --reload

# Or run directly
python -m examples.serving.api
```

## Endpoints

See [API documentation](../README.md) for endpoint details.
