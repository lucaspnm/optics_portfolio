"""
Pupil Function, Point Spread Function, and Aberration Simulation

This script demonstrates how a pupil function maps to a focal-plane point spread
function (PSF). A circular aperture produces a diffraction-limited Airy-like PSF.
Adding phase aberrations across the pupil changes the focal-plane intensity pattern.

Conceptual model:

    pupil amplitude + pupil phase -> complex pupil field -> Fourier transform -> PSF

This is a scalar Fourier-optics simulation. It uses normalized coordinates and does
not include physical units, real lens prescriptions, polarization, or propagation
distance scaling.
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
# Coordinate grid
# -----------------------------------------------------------------------------

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
    # Parameters:
    #   X, Y: 2D coordinate arrays
    # Returns:
    #   R, theta: Normalized radial and angular coordinates
    R = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    return R, theta


# -----------------------------------------------------------------------------
# Pupil and aberration functions
# -----------------------------------------------------------------------------

def circular_pupil(X: np.ndarray, Y: np.ndarray, radius: float = 0.8) -> np.ndarray:
    # Create a circular pupil function
    # Parameters:
    #   X, Y: 2D coordinate arrays
    #   radius: Radius of the circular aperture (normalized)
    # Returns:
    #   pupil: 2D array representing the pupil function
    R, _ = polar_coordinates(X, Y)
    return (R <= radius).astype(float)

def defocus_aberration(
    X: np.ndarray, 
    Y: np.ndarray, 
    pupil_radius: float = 0.8,
    strength: float = 1.0,
) -> np.ndarray:
    # Create a defocus aberration phase pattern. The strength is 
    # in arbitrary radians. Positive and negative values correspond
    # to opposite signs of defocus.
    # Parameters:
    #   X, Y: 2D coordinate arrays
    #   pupil_radius: Radius of the circular aperture (normalized)
    #   strength: Strength of the defocus aberration (normalized)
    # Returns:
    #   phase: 2D array representing the phase aberration
    
    R, _ = polar_coordinates(X, Y)
    # Normalize radial coordinate to pupil radius
    rho = R / pupil_radius  

    # Zernike defocus term
    phase = strength * (2 * rho**2 - 1)  
    # Zero phase outside the pupil
    phase[R > pupil_radius] = 0.0  

    return phase

def astigmatism_aberration(
    X: np.ndarray, 
    Y: np.ndarray, 
    pupil_radius: float = 0.8,
    strength: float = 1.0,
) -> np.ndarray:
    # Create an astigmatism aberration phase pattern. The strength is 
    # in arbitrary radians. Positive and negative values correspond
    # to opposite signs of astigmatism.
    # Parameters:
    #   X, Y: 2D coordinate arrays
    #   pupil_radius: Radius of the circular aperture (normalized)
    #   strength: Strength of the astigmatism aberration (normalized)
    # Returns:
    #   phase: 2D array representing the phase aberration
    
    R, theta = polar_coordinates(X, Y)
    rho = R / pupil_radius  

    # Zernike astigmatism term
    phase = strength * rho**2 * np.cos(2 * theta)  
    phase[R > pupil_radius] = 0.0  

    return phase

def coma_aberration(
    X: np.ndarray, 
    Y: np.ndarray, 
    pupil_radius: float = 0.8,
    strength: float = 1.0,
) -> np.ndarray:
    # Create a coma aberration phase pattern. The strength is 
    # in arbitrary radians. Positive and negative values correspond
    # to opposite signs of coma.
    # Parameters:
    #   X, Y: 2D coordinate arrays
    #   pupil_radius: Radius of the circular aperture (normalized)
    #   strength: Strength of the coma aberration (normalized)
    # Returns:
    #   phase: 2D array representing the phase aberration
    
    R, theta = polar_coordinates(X, Y)
    rho = R / pupil_radius  

    # Zernike coma term
    phase = strength * ( 3 * rho**3 - 2 * rho) * np.cos(theta)
    phase[R > pupil_radius] = 0.0  

    return phase

def make_pupil_field(
    aperture: np.ndarray,
    phase: np.ndarray,
) -> np.ndarray:
    # Create a complex pupil field with optional aberrations
    # The aperture controls amplitude transmission. 
    # The phase term represents wavefront error across the pupil. 
    # The resulting pupil field is a complex array.
    # Parameters:
    #   aperture: 2D array representing the pupil amplitude (0 or 1)
    #   phase: 2D array representing the pupil phase (in radians)
    # Returns:
    #   pupil_field: 2D complex array representing the pupil field
    pupil_field = aperture * np.exp(1j * phase)
    return pupil_field

# -----------------------------------------------------------------------------
# PSF calculation
# -----------------------------------------------------------------------------

def centered_fft2(field: np.ndarray) -> np.ndarray:
    # Compute the centered 2D inverse FFT of a field.
    return np.fft.fftshift(np.fft.fft2(field))

def normalize_image(image: np.ndarray) -> np.ndarray:
    # Normalize an image to the range [0, 1].
    image = np.abs(image)
    max_val = np.max(image)
    
    if max_val == 0:
        return image
    
    return image / max_val

def calculate_psf(pupil_field: np.ndarray) -> np.ndarray:
    # Calculate the point spread function (PSF) from a pupil field.
    # The PSF is the squared magnitude of the Fourier transform of the pupil field.
    # Parameters:
    #   pupil_field: 2D complex array representing the pupil field
    # Returns:
    #   psf: 2D array representing the point spread function
    field_ft = centered_fft2(pupil_field)
    psf = np.abs(field_ft) ** 2
    return normalize_image(psf)

def log_display(image: np.ndarray, scale: float = 1000.0) -> np.ndarray:
    # Return the log-scaled display for an image
    # PSFs have large dynamic range so log display makes sidelobes visible
    return np.log1p(scale * normalize_image(image))


# -----------------------------------------------------------------------------
# Plotting helpers
# -----------------------------------------------------------------------------

def save_figure(fig: plt.Figure, filename: str) -> None:
    # Save a figure to the figures directory.
    out_path = FIG_DIR / filename
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved figure to {out_path}")

def plot_pupil_phase_psf(
    aperture: np.ndarray,
    phase: np.ndarray,
    psf: np.ndarray,
    title: str, 
    filename: str,
) -> None:
    # Plot pupil amplitude, pupil phase, and focal-plane PSF.
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))

    axes[0].imshow(aperture, cmap="gray", origin="lower")
    axes[0].set_title("Pupil amplitude")
    axes[0].axis("off")

    phase_plot = axes[1].imshow(phase, cmap="twilight", origin="lower")
    axes[1].set_title("Pupil phase")
    axes[1].axis("off")
    fig.colorbar(phase_plot, ax=axes[1], fraction=0.046, pad=0.04)

    axes[2].imshow(log_display(psf), cmap="gray", origin="lower")
    axes[2].set_title("Focal-plane PSF")
    axes[2].axis("off")

    fig.suptitle(title)
    fig.tight_layout()

    save_figure(fig, filename)

def plot_psf_comparison(
    psfs: dict[str, np.ndarray],
    title: str,
    filename: str,
) -> None:
    # Compare several PSFs side by side
    fig, axes = plt.subplots(1, len(psfs), figsize=(4 * len(psfs), 4))

    for ax, (label, psf) in zip(axes, psfs.items()):
        ax.imshow(log_display(psf), cmap="gray", origin="lower")
        ax.set_title(label)
        ax.axis("off")

    fig.suptitle(title)
    fig.tight_layout()

    save_figure(fig, filename)


# -----------------------------------------------------------------------------
# Main demo
# -----------------------------------------------------------------------------

def main() -> None:
    # Run the pupil/PSF/aberration simulations
    n = 512
    pupil_radius = 0.8
    
    X, Y = make_coordinate_grid(n=n, extent=1.0)
    aperture = circular_pupil(X, Y, radius=pupil_radius)

    # Diffraction-limited case
    phase_flat = np.zeros_like(X)
    pupil_field = make_pupil_field(aperture, phase_flat)
    psf_diffraction_limited = calculate_psf(pupil_field)

    plot_pupil_phase_psf(
        aperture=aperture,
        phase=phase_flat,
        psf=psf_diffraction_limited,
        title="Diffraction-limited circular pupil",
        filename="diffraction_limited_psf.png",
    )

    # Defocus
    phase_defocus = defocus_aberration(
        X,
        Y, 
        pupil_radius=pupil_radius,
        strength=4.0,
    )
    
    pupil_field = make_pupil_field(aperture, phase_defocus)
    psf_defocus = calculate_psf(pupil_field)

    plot_pupil_phase_psf(
        aperture=aperture,
        phase=phase_defocus,
        psf=psf_defocus,
        title="Defocus aberration",
        filename="defocus_psf.png",
    )

    # Astigmatism 
    phase_astigmatism = astigmatism_aberration(
        X,
        Y,
        pupil_radius=pupil_radius,
        strength=4.0,
    )
    pupil_field = make_pupil_field(aperture, phase_astigmatism)
    psf_astigmatism = calculate_psf(pupil_field)

    plot_pupil_phase_psf(
        aperture=aperture,
        phase=phase_astigmatism,
        psf=psf_astigmatism,
        title="Astigmatism aberration",
        filename="astigmatism_psf.png",
    )

    # Coma
    phase_coma = coma_aberration(
        X,
        Y,
        pupil_radius=pupil_radius,
        strength=4.0,
    )
    pupil_field = make_pupil_field(aperture, phase_coma)
    psf_coma = calculate_psf(pupil_field)

    plot_pupil_phase_psf(
        aperture=aperture,
        phase=phase_coma,
        psf=psf_coma,
        title="Coma aberration",
        filename="coma_psf.png",
    )

    # Compare all PSFs
    psfs = {
        "Diffraction-limited": psf_diffraction_limited,
        "Defocus": psf_defocus,
        "Astigmatism": psf_astigmatism,
        "Coma": psf_coma,
    }

    plot_psf_comparison(
        psfs=psfs,
        title="Effect of pupil phase aberrations on focal-plane PSF",
        filename="psf_aberration_comparison.png",
    )

    # Ideal correction example: apply the opposite phase to cancel coma
    corrected_phase = phase_coma - phase_coma
    corrected_field = make_pupil_field(aperture, corrected_phase)
    psf_corrected = calculate_psf(corrected_field)

    psfs = {
        "Diffraction-limited": psf_diffraction_limited,
        "Coma": psf_coma,
        "Ideal correction": psf_corrected,
    }

    plot_psf_comparison(
        psfs=psfs,
        title="Ideal phase correction of coma",
        filename="ideal_coma_correction.png",
    )


if __name__ == "__main__":
    main()