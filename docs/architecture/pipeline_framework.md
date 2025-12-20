# Pipeline Framework

## Purpose

Design and implementation of the pipeline processing framework.

## Pipeline Architecture

```mermaid
graph LR
    A[Source] --> B[Reader]
    B --> C[Preprocessor]
    C --> D[Tiler]
    D --> E[Inference]
    E --> F[Postprocessor]
    F --> G[Writer]
    G --> H[Sink]
```

## Pipeline Definition

$$
P = (S, R, \text{Pre}, T, I, \text{Post}, W, O)
$$

| Stage | Input | Output | Configuration |
|-------|-------|--------|---------------|
| Source | Path | URI | path, format |
| Reader | URI | Array | driver, bands |
| Preprocessor | Array | Tensor | normalize, augment |
| Tiler | Tensor | Batches | size, overlap |
| Inference | Batches | Predictions | model, device |
| Postprocessor | Predictions | Results | threshold, NMS |
| Writer | Results | File | format, CRS |
| Sink | File | Path | compression |

## Configuration

```yaml
pipeline:
  name: ship_detection
  stages:
    - reader:
        driver: rasterio
        bands: [1, 2, 3]
    - preprocessor:
        normalize: true
        mean: [0.485, 0.456, 0.406]
    - tiler:
        size: 256
        overlap: 32
    - inference:
        model: ship_detector_base
        device: auto
    - postprocessor:
        threshold: 0.5
        nms_iou: 0.3
    - writer:
        format: geotiff
```

## Extensibility

Create custom stages by implementing:

```python
from unbihexium.pipeline import Stage

class CustomStage(Stage):
    def process(self, data):
        # Transform data
        return transformed
```
