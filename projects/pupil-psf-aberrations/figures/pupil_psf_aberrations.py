"""
Pupil Function, Point Spread Function, and Aberration Simulation

This script demonstrates how a pupil function maps to a focal-plane point spread 
function (PSF). A circular aperture produces a diffraction-limited Airy-like PSF. 
Adding phase aberrations across the pupil changes the focal-plane intensity pattern.

Conceptual model:

    pupil amplitude + pupil phase -> complex pupil field -> Fourier Transform -> PSF

This is a scalar Fourier-optics simulation. It uses normalized coordinates and does 
not include physical units, real lens prescriptions, polarization, or propagation 
distance scaling.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Configuration
# -----------------------------

FIG_DIR = Path(__file__).resolve().parent / "figures"
FIG_DIR.mkdir(exist_ok=True)

# -----------------------------
# Coordinate grid
# -----------------------------

def make_coordinate_grid(n: int = 512, extent: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    # Create a normalized 2D coordinate grid
    # Parameters:
    #   n: Number of samples along each dimension
    #   extent: Grid runs from -extent to +extent in both x and y
    # Returns:
    #   X, Y: 2D coordinate arrays
    x = np.linspace(-extent, extent, n)
    X, Y = np.meshgrid(x, x)
    return X, Y

def polar_coordinates(X: np.ndarray, Y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # Return normalized radial and angular coordinates
    R = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    return R, theta

# -----------------------------
# Pupil and aberration functions
# -----------------------------

def circular_pupil(X: np.ndarray, Y: np.ndarray)
