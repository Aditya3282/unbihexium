# Notebooks

[![CI](https://github.com/unbihexium-oss/unbihexium/workflows/CI/badge.svg)](https://github.com/unbihexium-oss/unbihexium/actions)
[![PyPI](https://img.shields.io/pypi/v/unbihexium.svg)](https://pypi.org/project/unbihexium/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](../../LICENSE.txt)

## Purpose

Interactive Jupyter notebooks demonstrating Unbihexium capabilities.

## Notebook Index

```mermaid
graph LR
    A[01 Getting Started] --> B[02 Detection]
    A --> C[03 Indices]
    B --> D[04 Change]
    C --> E[05 Risk]
    D --> F[06 Segmentation]
```

## Prerequisites

$$\text{Setup Time} \approx 15 \text{ minutes}$$

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| unbihexium | 1.0.0+ |
| onnxruntime | 1.15+ |
| numpy | 1.24+ |

## Available Notebooks

| Notebook | Topic | Duration |
|----------|-------|----------|
| [01_getting_started.ipynb](01_getting_started.ipynb) | Installation and basics | 15 min |
| [02_object_detection.ipynb](02_object_detection.ipynb) | Ship, building, vehicle detection | 20 min |
| [03_spectral_indices.ipynb](03_spectral_indices.ipynb) | NDVI, NDWI, SAVI calculation | 15 min |
| [04_change_detection.ipynb](04_change_detection.ipynb) | Bi-temporal change analysis | 20 min |
| [05_risk_assessment.ipynb](05_risk_assessment.ipynb) | Flood, wildfire, hazard risk | 25 min |
| [06_segmentation.ipynb](06_segmentation.ipynb) | LULC, crop classification | 20 min |

## Running Notebooks

```bash
# Install Jupyter
pip install jupyter

# Start notebook server
jupyter notebook examples/notebooks/

# Or use JupyterLab
pip install jupyterlab
jupyter lab examples/notebooks/
```

## Learning Path

1. Start with **01_getting_started** to verify installation
2. Choose a domain notebooks based on your use case
3. Each notebook includes formulas, examples, and exercises

---

**Copyright 2025 Unbihexium OSS Foundation. Apache-2.0 License.**
