"""
Fourier Optics and 4F Relay Simulation

This script simulates an idealized 4F optical system:

Input image plane -> Fourier plane -> Output image plane

In a physical 4F relay, the first lens maps the input field into a Fourier plane,
where transverse position corresponds to spatial-frequency content or propagation angle. 
A mask placed in that Fourier plane modifies the spatial frequency content. 
The second lens maps the filtered field back to an output image plane.

This is a scalar, conceptual Fourier-optics demo. It does not include real physical 
units, finite lens apertures, polarization, diffraction efficiency, or propagation 
distance scaling. 
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

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

def radial_coordinate(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    # Return the radial coordinate on a 2D grid
    return np.sqrt(X**2 + Y**2)

# -----------------------------
# Object generators
# -----------------------------

def circular_aperture(X: np.ndarray, Y: np.ndarray, radius: float = 0.25) -> np.ndarray:
    # Create a circular aperture object
    R = radial_coordinate(X, Y)
    return (R < radius).astype(float)

def double_slit(
    X: np.ndarray,
    Y: np.ndarray,
    slit_width: float = 0.04,
    slit_height: float = 0.65,
    separation: float = 0.28,
) -> np.ndarray:
    # Create a double slit object
    slit1 = (np.abs(X - separation/2) < slit_width/2) & (np.abs(Y) < slit_height/2)
    slit2 = (np.abs(X + separation/2) < slit_width/2) & (np.abs(Y) < slit_height/2)
    return (slit1 | slit2).astype(float)

def checkerboard(
    X: np.ndarray,
    Y: np.ndarray,
    num_checks: int = 16,
    window_radius: float = 0.85,
) -> np.ndarray:
    # Create a checkerboard pattern object inside a circular window
    # The circular window makes the finite-array boundary 
    # less dominant in the Fourier plane.

    ix = np.floor((X + 1) / 2 * num_checks).astype(int)
    iy = np.floor((Y + 1) / 2 * num_checks).astype(int)
    board = ((ix + iy) % 2 == 0).astype(float)

    R = radial_coordinate(X, Y)
    window = (R < window_radius).astype(float)
    return board * window

def letter_l(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    # Create a letter "L" object
    vertical = (X > -0.55) & (X < -0.35) & (Y > -0.55) & (Y < 0.55)
    horizontal = (X > -0.55) & (X < 0.35) & (Y > -0.55) & (Y < -0.35)
    return (vertical | horizontal).astype(float)

def vertical_grating(
    X: np.ndarray,
    Y: np.ndarray,
    period: float = 0.18,
    duty_cycle: float = 0.5,
    window_radius: float = 0.85,
) -> np.ndarray:
    # Create a vertical bar grating object
    # Vertical bars vary in x, so the Fourier content is primarily along kx.
    
    phase = ((X + 1.0) % period) / period
    grating = (phase < duty_cycle).astype(float)

    R = radial_coordinate(X, Y)
    window = (R < window_radius).astype(float)
    
    return grating * window

def horizontal_grating(
    X: np.ndarray,
    Y: np.ndarray,
    period: float = 0.18,
    duty_cycle: float = 0.5,
    window_radius: float = 0.85,
) -> np.ndarray:
    # Create a horizontal bar grating object
    # Horizontal bars vary in y, so the Fourier content is primarily along ky.
    
    phase = ((Y + 1.0) % period) / period
    grating = (phase < duty_cycle).astype(float)

    R = radial_coordinate(X, Y)
    window = (R < window_radius).astype(float)
    
    return grating * window


# -----------------------------
# Fourier optics functions
# -----------------------------

def centered_fft2(field: np.ndarray) -> np.ndarray:
    # Compute the centered 2D FFT of a field.
    return np.fft.fftshift(np.fft.fft2(field))

def centered_ifft2(field: np.ndarray) -> np.ndarray:
    # Compute the centered 2D inverse FFT of a field.
    return np.fft.ifft2(np.fft.ifftshift(field))

def normalize_image(image: np.ndarray) -> np.ndarray:
    # Normalize an image to the range [0, 1].
    image = np.abs(image)
    max_val = np.max(image)
    
    if max_val == 0:
        return image
    
    return image / max_val

def fourier_plane_display(field: np.ndarray) -> np.ndarray:
    # Return the log-scaled Fourier plane intensity for display.
    # The actual Fourier plane can have a very large dynamic range, so log scaling makes
    # weaker spatial frequency features visible.
    F = centered_fft2(field)
    intensity = np.abs(F)**2
    return np.log1p(intensity)  # Use log1p for better visualization

def apply_fourier_filter(field: np.ndarray, mask: np.ndarray) -> np.ndarray:
    spectrum = centered_fft2(field)
    filtered_spectrum = spectrum * mask
    output = centered_ifft2(filtered_spectrum)
    return normalize_image(output)

# -----------------------------
# Fourier-plane filter generators
# -----------------------------

def low_pass_filter(X: np.ndarray, Y: np.ndarray, cutoff_radius: float = 0.18) -> np.ndarray:
    # Pass low spatial frequencies near the center of the Fourier plane
    R = radial_coordinate(X, Y)
    return (R < cutoff_radius).astype(float)

def high_pass_filter(X: np.ndarray, Y: np.ndarray, cutoff_radius: float = 0.10) -> np.ndarray:
    # Pass high spatial frequencies away from the center of the Fourier plane
    R = radial_coordinate(X, Y)
    return (R > cutoff_radius).astype(float)

def horizontal_bandpass_filter(X: np.ndarray, Y: np.ndarray, width: float = 0.08) -> np.ndarray:
    # Pass horizontal spatial frequencies in a band around the center
    return (np.abs(Y) < width).astype(float)

def vertical_bandpass_filter(X: np.ndarray, Y: np.ndarray, width: float = 0.08) -> np.ndarray:
    # Pass vertical spatial frequencies in a band around the center
    return (np.abs(X) < width).astype(float)

def annular_filter(
    X: np.ndarray, 
    Y: np.ndarray, 
    inner_radius: float = 0.08, 
    outer_radius: float = 0.28,
) -> np.ndarray:
    # Pass intermediate spatial frequencies in an annular region
    R = radial_coordinate(X, Y)
    return ((R > inner_radius) & (R < outer_radius)).astype(float)

# -----------------------------
# Plotting helpers
# -----------------------------

def save_and_show(fig: plt.Figure, filename: str) -> None:
    # Save a Matplotlib figure and display it.
    out_path = FIG_DIR / filename
    fig.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved figure to {out_path}")

def plot_single_filter_demo(
    field: np.ndarray,
    mask: np.ndarray,
    title: str,
    filename: str,
) -> None:
    """Plot input plane, Fourier plane intensity, Fourier-plane mask, and output plane."""
    output = apply_fourier_filter(field, mask)

    fig, axes = plt.subplots(1, 4, figsize=(14, 4))

    axes[0].imshow(field, cmap="gray", origin="lower")
    axes[0].set_title("Input image plane")
    axes[0].axis("off")

    axes[1].imshow(fourier_plane_display(field), cmap="gray", origin="lower")
    axes[1].set_title("Fourier plane intensity")
    axes[1].axis("off")

    axes[2].imshow(mask, cmap="gray", origin="lower")
    axes[2].set_title("Fourier plane mask")
    axes[2].axis("off")

    axes[3].imshow(output, cmap="gray", origin="lower")
    axes[3].set_title("Output image plane")
    axes[3].axis("off")

    fig.suptitle(title)
    fig.tight_layout()

    save_and_show(fig, filename)


def plot_multi_filter_demo(
    field: np.ndarray,
    filters: dict[str, np.ndarray],
    title: str,
    filename: str,
) -> None:
    """Plot the same input object after multiple Fourier-plane filters."""
    num_filters = len(filters)

    fig, axes = plt.subplots(
        2,
        num_filters + 1,
        figsize=(4 * (num_filters + 1), 8),
    )

    axes[0, 0].imshow(field, cmap="gray", origin="lower")
    axes[0, 0].set_title("Input image plane")
    axes[0, 0].axis("off")

    axes[1, 0].imshow(fourier_plane_display(field), cmap="gray", origin="lower")
    axes[1, 0].set_title("Fourier plane intensity")
    axes[1, 0].axis("off")

    for col, (filter_name, mask) in enumerate(filters.items(), start=1):
        output = apply_fourier_filter(field, mask)

        axes[0, col].imshow(mask, cmap="gray", origin="lower")
        axes[0, col].set_title(filter_name)
        axes[0, col].axis("off")

        axes[1, col].imshow(output, cmap="gray", origin="lower")
        axes[1, col].set_title("Output image plane")
        axes[1, col].axis("off")

    fig.suptitle(title)
    fig.tight_layout()

    save_and_show(fig, filename)

# -----------------------------
# Main demo
# -----------------------------

def main() -> None:
    # Run all Fourier filtering demos and save figures.
    N = 512
    X, Y = make_coordinate_grid(n=N, extent=1.0)
    
    # Demo 1: circular aperture with low-pass filter
    field = circular_aperture(X, Y, radius=0.25)
    mask = low_pass_filter(X, Y, cutoff_radius=0.18)

    plot_single_filter_demo(
        field=field,
        mask=mask,
        title="Circular aperture: low-pass filtering in the Fourier plane",
        filename="circular_aperture_low_pass.png",
    )

    # Demo 2: double slit with multiple filters
    field = double_slit(X, Y)

    filters = {
        "Low-pass mask": low_pass_filter(X, Y, cutoff_radius=0.16),
        "High-pass mask": high_pass_filter(X, Y, cutoff_radius=0.08),
        "Annular mask": annular_filter(X, Y, inner_radius=0.08, outer_radius=0.28),
    }

    plot_multi_filter_demo(
        field=field,
        filters=filters,
        title="Double slit: multiple Fourier-plane filters",
        filename="double_slit_multi_filters.png",
    )

    # Demo 3: Checkerboard with multiple filters
    field = checkerboard(X, Y, num_checks=18)

    filters = {
        "Low-pass mask": low_pass_filter(X, Y, cutoff_radius=0.14),
        "High-pass mask": high_pass_filter(X, Y, cutoff_radius=0.10),
        "Horizontal band": horizontal_bandpass_filter(X, Y, width=0.08),
        "Vertical band": vertical_bandpass_filter(X, Y, width=0.08),
    }

    plot_multi_filter_demo(
        field=field,
        filters=filters,
        title="Checkerboard: multiple Fourier-plane filters",
        filename="checkerboard_multi_filters.png",
    )

    # Demo 4: Letter "L" with multiple filters
    field = letter_l(X, Y)

    filters = {
        "Low-pass mask": low_pass_filter(X, Y, cutoff_radius=0.15),
        "High-pass mask": high_pass_filter(X, Y, cutoff_radius=0.08),
        "Annular mask": annular_filter(X, Y, inner_radius=0.08, outer_radius=0.30),
    }

    plot_multi_filter_demo(
        field=field,
        filters=filters,
        title="Letter 'L': multiple Fourier-plane filters",
        filename="letter_l_multi_filters.png",
    )

    # Demo 5: Vertical and horizontal gratings with multiple filters
    field = vertical_grating(X, Y, period=0.16)

    filters = {
        "Low-pass mask": low_pass_filter(X, Y, cutoff_radius=0.14),
        "Horizontal band": horizontal_bandpass_filter(X, Y, width=0.07),
        "Vertical band": vertical_bandpass_filter(X, Y, width=0.07),
    }

    plot_multi_filter_demo(
        field=field,
        filters=filters,
        title="Vertical grating: directional spatial frequency filtering",
        filename="vertical_grating_multi_filters.png",
    )

    field = horizontal_grating(X, Y, period=0.16)

    filters = {
        "Low-pass mask": low_pass_filter(X, Y, cutoff_radius=0.14),
        "Horizontal band": horizontal_bandpass_filter(X, Y, width=0.07),
        "Vertical band": vertical_bandpass_filter(X, Y, width=0.07),
    }

    plot_multi_filter_demo(
        field=field,
        filters=filters,
        title="Horizontal grating: directional spatial frequency filtering",
        filename="horizontal_grating_multi_filters.png",
    )

if __name__ == "__main__":
    main()