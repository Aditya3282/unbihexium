# Architecture Overview

## Purpose

System architecture documentation for Unbihexium.

## High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface"
        A1[CLI]
        A2[Python API]
        A3[REST API]
    end
    
    subgraph "Application Layer"
        B1[Pipeline Orchestrator]
        B2[Capability Registry]
        B3[Configuration Manager]
    end
    
    subgraph "Core Services"
        C1[Model Zoo Manager]
        C2[Inference Engine]
        C3[Tile Processor]
        C4[Georeferencer]
    end
    
    subgraph "Data Layer"
        D1[Model Cache]
        D2[Tile Store]
        D3[Result Store]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B2
    B2 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> D3
    C1 --> D1
    C3 --> D2
```

## Component Responsibilities

$$
\text{System} = \bigcup_{i=1}^{n} \text{Component}_i \quad \text{where} \quad \bigcap_{i \neq j} \text{Component}_i \cap \text{Component}_j = \emptyset
$$

| Component | Responsibility | Dependencies |
|-----------|---------------|--------------|
| Pipeline Orchestrator | Workflow execution | Registry, Config |
| Capability Registry | Capability lookup | Model Zoo |
| Model Zoo Manager | Model lifecycle | Cache |
| Inference Engine | ONNX execution | Tile Processor |
| Tile Processor | Image tiling | Georeferencer |
| Georeferencer | CRS handling | GDAL/Rasterio |

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Pipeline
    participant TileProcessor
    participant InferenceEngine
    participant Output
    
    User->>Pipeline: Execute
    Pipeline->>TileProcessor: Tile image
    loop Each tile
        TileProcessor->>InferenceEngine: Process tile
        InferenceEngine-->>TileProcessor: Predictions
    end
    TileProcessor->>Output: Merge and save
    Output-->>User: Result
```

## Design Principles

1. **Modularity**: Independent components
2. **Extensibility**: Plugin architecture
3. **Consistency**: Uniform interfaces
4. **Observability**: Logging and metrics
5. **Resilience**: Error handling

## Technology Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Inference | ONNX Runtime |
| Geospatial | GDAL, Rasterio, Shapely |
| CLI | Click, Rich |
| Testing | PyTest |
| Linting | Ruff, Pyright |
