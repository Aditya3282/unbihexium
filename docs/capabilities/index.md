# Capabilities Encyclopedia

## Purpose

This index provides navigation to the 12 capability domains implemented in Unbihexium.

## Audience

- Solution architects evaluating coverage
- Developers implementing pipelines
- Analysts selecting appropriate models
- Integration engineers mapping requirements

## Capability Architecture

```mermaid
graph TB
    subgraph "Sensing Layer"
        A1[Optical Imagery]
        A2[SAR Imagery]
        A3[Aerial Data]
    end
    
    subgraph "AI Capabilities"
        B1[Detection]
        B2[Segmentation]
        B3[Change Analysis]
        B4[Regression]
        B5[Enhancement]
    end
    
    subgraph "Domain Applications"
        C1[Defense/Intelligence]
        C2[Agriculture]
        C3[Urban Planning]
        C4[Environment]
        C5[Energy/Assets]
        C6[Risk/Insurance]
    end
    
    A1 --> B1
    A1 --> B2
    A2 --> B3
    A3 --> B4
    A1 --> B5
    
    B1 --> C1
    B2 --> C2
    B3 --> C3
    B4 --> C4
    B5 --> C5
    B1 --> C6
```

## Coverage Formula

Total capability coverage measured as:

$$
C_{\text{total}} = \frac{\sum_{d=1}^{12} \sum_{c \in D_d} \mathbb{1}[\text{implemented}(c)]}{N_{\text{required}}} \times 100\%
$$

## Capability Matrix

| ID | Domain | Implementations | Models | Status |
|----|--------|-----------------|--------|--------|
| 01 | [AI Products](01_ai_products.md) | 13 | 39 | Production |
| 02 | [Tourism and Data Processing](02_tourism_data_processing.md) | 18 | 30 | Production |
| 03 | [Indices and Flood/Water](03_indices_flood_water.md) | 13 | 36 | Production |
| 04 | [Environment and Forestry](04_environment_forestry_image_processing.md) | 24 | 42 | Production |
| 05 | [Asset Management and Energy](05_asset_management_energy.md) | 16 | 36 | Production |
| 06 | [Urban and Agriculture](06_urban_agriculture.md) | 26 | 54 | Production |
| 07 | [Risk and Defense (Neutral)](07_risk_defense_neutral.md) | 17 | 45 | Production |
| 08 | [Value-Added Imagery](08_value_added_imagery.md) | 3 | 9 | Production |
| 09 | [Benefits Narrative](09_benefits_narrative.md) | N/A | N/A | Documentation |
| 10 | [Satellite Imagery Features](10_satellite_imagery_features.md) | 7 | 21 | Production |
| 11 | [Resolution and Metadata QA](11_resolution_metadata_qa.md) | 4 | 12 | Production |
| 12 | [Radar and SAR](12_radar_sar.md) | 7 | 21 | Research |

## Implementation Status

```mermaid
pie title Implementation Status
    "Production" : 11
    "Research" : 1
    "Documentation" : 1
```

## Cross-Domain Dependencies

```mermaid
flowchart LR
    A[Input Processing] --> B[Indices 03]
    B --> C[Environment 04]
    B --> D[Agriculture 06]
    C --> E[Risk 07]
    D --> E
    
    F[Detection 01] --> G[Urban 06]
    F --> H[Defense 07]
    F --> I[Assets 05]
```

## Quick Reference

| Capability | Primary Use Case | Entry Point |
|------------|------------------|-------------|
| Super-resolution | Image enhancement | `pipeline.run("super_resolution")` |
| Ship detection | Maritime awareness | `pipeline.run("ship_detection")` |
| NDVI calculation | Vegetation health | `pipeline.run("ndvi")` |
| Flood risk | Hazard assessment | `pipeline.run("flood_risk")` |
| Change detection | Temporal analysis | `pipeline.run("change_detection")` |
