#!/usr/bin/env python3
"""Export SRCNN model to ONNX format.

This script exports a trained SRCNN model to ONNX for cross-platform inference.

Usage:
    python scripts/export_srcnn_onnx.py --input srcnn.pt --output srcnn.onnx

Example:
    python scripts/export_srcnn_onnx.py --input model.pt --output model.onnx --opset 14
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import torch
except ImportError as e:
    print("PyTorch is required. Install with: pip install torch")
    raise SystemExit(1) from e

from unbihexium.ai.super_resolution.srcnn import SRCNN, SRCNNConfig


def export_to_onnx(
    model_path: Path,
    output_path: Path,
    opset_version: int = 14,
    input_size: tuple[int, int] = (64, 64),
) -> None:
    """Export PyTorch SRCNN model to ONNX.

    Args:
        model_path: Path to PyTorch model checkpoint.
        output_path: Path for ONNX output file.
        opset_version: ONNX opset version.
        input_size: Input image size (H, W).
    """
    print(f"Loading model from: {model_path}")

    # Load checkpoint
    checkpoint = torch.load(model_path, map_location="cpu")

    # Reconstruct model
    config = checkpoint.get("config", SRCNNConfig())
    model = SRCNN(config)
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()

    print(f"Model loaded. Config: scale={config.scale_factor}")

    # Create dummy input
    batch_size = 1
    channels = config.input_channels
    h, w = input_size
    dummy_input = torch.randn(batch_size, channels, h, w)

    print(f"Exporting to ONNX with input shape: {dummy_input.shape}")

    # Export
    torch.onnx.export(
        model,
        dummy_input,
        str(output_path),
        opset_version=opset_version,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input": {0: "batch_size", 2: "height", 3: "width"},
            "output": {0: "batch_size", 2: "height", 3: "width"},
        },
    )

    print(f"ONNX model saved to: {output_path}")

    # Verify export
    try:
        import onnx

        onnx_model = onnx.load(str(output_path))
        onnx.checker.check_model(onnx_model)
        print("ONNX model verification: PASSED")
    except ImportError:
        print("Install onnx for model verification: pip install onnx")
    except Exception as e:
        print(f"ONNX verification failed: {e}")


def create_dummy_model(output_path: Path, scale_factor: int = 2) -> None:
    """Create and export a dummy SRCNN model for testing.

    Args:
        output_path: Path to save the ONNX model.
        scale_factor: Super-resolution scale factor.
    """
    print(f"Creating dummy SRCNN model with scale={scale_factor}")

    config = SRCNNConfig(scale_factor=scale_factor)
    model = SRCNN(config)
    model.eval()

    # Create dummy input
    dummy_input = torch.randn(1, 3, 64, 64)

    # Export directly
    torch.onnx.export(
        model,
        dummy_input,
        str(output_path),
        opset_version=14,
        input_names=["input"],
        output_names=["output"],
    )

    print(f"Dummy ONNX model saved to: {output_path}")


def main() -> None:
    """Main export function."""
    parser = argparse.ArgumentParser(description="Export SRCNN to ONNX")
    parser.add_argument("--input", type=str, help="Input PyTorch model path")
    parser.add_argument(
        "--output", type=str, default="srcnn.onnx", help="Output ONNX path"
    )
    parser.add_argument("--opset", type=int, default=14, help="ONNX opset version")
    parser.add_argument(
        "--dummy", action="store_true", help="Create dummy model (no training required)"
    )
    parser.add_argument("--scale", type=int, default=2, help="Scale factor for dummy")
    args = parser.parse_args()

    output_path = Path(args.output)

    if args.dummy:
        create_dummy_model(output_path, scale_factor=args.scale)
    else:
        if not args.input:
            parser.error("--input is required when not using --dummy")
        export_to_onnx(
            Path(args.input),
            output_path,
            opset_version=args.opset,
        )


if __name__ == "__main__":
    main()
