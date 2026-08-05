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

    r_Airy
    
    """
