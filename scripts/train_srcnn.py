#!/usr/bin/env python3
"""Training script for SRCNN super-resolution model.

This script trains an SRCNN model on synthetic data for demonstration.
For production use, replace with real satellite imagery datasets.

Usage:
    python scripts/train_srcnn.py --epochs 10 --scale 2 --output model.pt

Example:
    python scripts/train_srcnn.py --epochs 50 --scale 4 --output srcnn_4x.pt
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, Dataset
except ImportError as e:
    print("PyTorch is required. Install with: pip install torch")
    raise SystemExit(1) from e

from unbihexium.ai.super_resolution.srcnn import SRCNN, SRCNNConfig, compute_psnr


class SyntheticSRDataset(Dataset):
    """Synthetic dataset for super-resolution training."""

    def __init__(
        self,
        num_samples: int = 100,
        image_size: int = 64,
        scale_factor: int = 2,
        seed: int = 42,
    ) -> None:
        """Initialize synthetic dataset.

        Args:
            num_samples: Number of samples to generate.
            image_size: Size of HR images (square).
            scale_factor: Downscaling factor for LR images.
            seed: Random seed for reproducibility.
        """
        self.num_samples = num_samples
        self.image_size = image_size
        self.scale_factor = scale_factor

        np.random.seed(seed)
        self.data = self._generate_data()

    def _generate_data(self) -> list[tuple[np.ndarray, np.ndarray]]:
        """Generate synthetic LR-HR pairs."""
        from scipy.ndimage import zoom

        data = []
        for _ in range(self.num_samples):
            # Generate HR image with some structure
            hr = np.random.rand(3, self.image_size, self.image_size).astype(np.float32)

            # Add some patterns
            x = np.linspace(0, 4 * np.pi, self.image_size)
            y = np.linspace(0, 4 * np.pi, self.image_size)
            xx, yy = np.meshgrid(x, y)
            pattern = (np.sin(xx) * np.cos(yy) + 1) / 2
            hr[0] = 0.5 * hr[0] + 0.5 * pattern.astype(np.float32)

            # Create LR by downsampling
            lr = zoom(
                hr,
                (1, 1 / self.scale_factor, 1 / self.scale_factor),
                order=1,
            ).astype(np.float32)

            data.append((lr, hr))

        return data

    def __len__(self) -> int:
        return self.num_samples

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        lr, hr = self.data[idx]
        return torch.from_numpy(lr), torch.from_numpy(hr)


def train_epoch(
    model: SRCNN,
    dataloader: DataLoader,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
) -> float:
    """Train for one epoch."""
    model.train()
    total_loss = 0.0

    for lr, hr in dataloader:
        lr = lr.to(device)
        hr = hr.to(device)

        optimizer.zero_grad()
        output = model(lr)
        loss = criterion(output, hr)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)


def validate(
    model: SRCNN,
    dataloader: DataLoader,
    device: torch.device,
) -> tuple[float, float]:
    """Validate model and compute PSNR."""
    model.eval()
    total_psnr = 0.0
    total_mse = 0.0

    with torch.no_grad():
        for lr, hr in dataloader:
            lr = lr.to(device)
            hr = hr.to(device)

            output = model(lr)

            # Compute metrics
            mse = nn.functional.mse_loss(output, hr).item()
            total_mse += mse

            # PSNR per batch
            output_np = output.cpu().numpy()
            hr_np = hr.cpu().numpy()
            for i in range(output_np.shape[0]):
                total_psnr += compute_psnr(output_np[i], hr_np[i])

    n_samples = len(dataloader.dataset)
    return total_mse / len(dataloader), total_psnr / n_samples


def main() -> None:
    """Main training function."""
    parser = argparse.ArgumentParser(description="Train SRCNN model")
    parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--scale", type=int, default=2, help="Scale factor")
    parser.add_argument(
        "--output", type=str, default="srcnn.pt", help="Output model path"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Set seeds
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    # Create datasets
    train_dataset = SyntheticSRDataset(
        num_samples=200,
        scale_factor=args.scale,
        seed=args.seed,
    )
    val_dataset = SyntheticSRDataset(
        num_samples=50,
        scale_factor=args.scale,
        seed=args.seed + 1,
    )

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    # Create model
    config = SRCNNConfig(scale_factor=args.scale)
    model = SRCNN(config).to(device)
    print(f"Model parameters: {model.count_parameters():,}")

    # Training setup
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    # Training loop
    best_psnr = 0.0
    for epoch in range(args.epochs):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_mse, val_psnr = validate(model, val_loader, device)

        print(
            f"Epoch {epoch + 1}/{args.epochs} - "
            f"Train Loss: {train_loss:.6f}, "
            f"Val MSE: {val_mse:.6f}, "
            f"Val PSNR: {val_psnr:.2f} dB"
        )

        if val_psnr > best_psnr:
            best_psnr = val_psnr
            torch.save(
                {
                    "config": config,
                    "state_dict": model.state_dict(),
                    "psnr": best_psnr,
                },
                args.output,
            )
            print(f"  Saved best model: {best_psnr:.2f} dB")

    print(f"Training complete. Best PSNR: {best_psnr:.2f} dB")
    print(f"Model saved to: {args.output}")


if __name__ == "__main__":
    main()
