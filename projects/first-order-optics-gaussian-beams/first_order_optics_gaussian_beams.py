"""
First-Order Optics and Gaussian Beam Calculator 

This script demonstrates several core first-order optics and Gaussian beam concepts:

thin-lens imaging 
F-number
numerical aperture
diffraction-limited Airy radius
Gaussian beam waist
Rayleigh range
beam divergence
telescope / beam expander behavior 

This goal of this project is to connect simple optical engineering calculations to practical system
design intuition. This is a scalar, paraxial optics model. It uses simplified formulas and does not
include aberrations, polarization, real lens prescriptions, alignment tolerances, or non-paraxial 
effects. 
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

FIG_DIR = Path(__file__).resolve().parent / "figures"
FIG_DIR.mkdir(exist_ok=True)

# -----------------------------------------------------------------------------
# First-order optics calculations
# -----------------------------------------------------------------------------

def thin_lens_image_distance(
    focal_length: float, 
    object_distance: float,
) -> float:
    """
    Calculate image distance using the thin lens equation. 

    1/f = 1/s + 1/s'

    Parameters
    ----------
    focal_length: 
        Lens focal length.
    object_distance:
        Object distance from the lens.

    
    Returns
    -------
    image_distance:
        Image distance from the lens
    """
    return 1.0 / ((1.0 / focal_length) - (1.0 / object_distance))

def transverse_magnification(
    object_distance: float,
    image_distance: float,
) -> float:
    """
    Calculate transverse magnification

        m = -s' / s
    """
    return -image_distance / object_distance

def f_number(
    focal_length: float,
    aperture_diameter: float,
) -> float:
    """
    Calculate F-number.

        F/# = f / D
    """
    return focal_length / aperture_diameter

def numerical_aperture_paraxial(
    aperture_diameter: float,
    focal_length: float,
) -> float:
    """
    Approximate numerical aperture in air for a focused beam.

        NA ~ D / (2f)

    This is a paraxial approximation
    """
    return aperture_diameter / (2.0 * focal_length)

def airy_radius(
    wavelength: float,
    focal_length: float,
    aperture_diameter: float,
) -> float:
    """
    Calculate diffraction-limited Airy disk radius to the first zero.

        r_Airy ~ 1.22 * lambda * f / D

    Parameters should use consistent units.
    """
    return 1.22 * wavelength * focal_length / aperture_diameter

def diffraction_limited_spot_diameter(
    wavelength: float,
    focal_length: float,
    aperture_diameter: float,
) -> float:
    """
    Calculate diffraction-limited Airy disk diameter to the first zero.
    
        diameter ~ 2.44 * lambda * f / D
    """
    return 2.0 * airy_radius(wavelength, focal_length, aperture_diameter)

# -----------------------------------------------------------------------------
# Gaussian beam calculations
# -----------------------------------------------------------------------------

def rayleigh_range(
    waist_radius: float,
    wavelength: float,
) -> float:
    """
    Calculate Gaussian beam Rayleigh range.

        z_R = pi * w0^2 / lambda
    """
    return np.pi * waist_radius**2 / wavelength

def gaussian_beam_radius(
    z: np.ndarray,
    waist_radius: float,
    wavelength: float,
) -> np.ndarray:
    """
    Calculate Gaussian beam radius as a function of propogation distance.

        w(z) = w0 * sqrt(1 + (z/z_R)^2 )
    """
    z_r = rayleigh_range(waist_radius, wavelength)
    return waist_radius * np.sqrt(1.0 + (z / z_r) ** 2)

def gaussian_divergence_half_angle(
    waist_radius: float,
    wavelength: float,
) -> float:
    """
    Calculate far-field Gaussian beam divergence half-angle.
    
        theta ~ lambda / (pi * w0)
    """
    return wavelength / np.pi * waist_radius

def beam_expander_output_divergence(
    input_divergence: float,
    focal_length_1: float,
    focal_length_2: float,
) -> float:
    """
    Calculate approximate output divergence after a beam expander.
    Beam expansion reduces divergence by the telescope magnification.

        theta_out = theta_in / M
    """
    magnification = focal_length_2 / focal_length_1
    return input_divergence / magnification

# -----------------------------------------------------------------------------
# Plotting helpers 
# -----------------------------------------------------------------------------

def save_figure(fig: plt.figure, filename: str) -> None:
    """Save a figure to the figures directory."""
    out_path = FIG_DIR / filename
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved figure to {out_path}")