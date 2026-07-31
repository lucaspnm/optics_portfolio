# Pupil Function, PSF, and Aberration Simulation

## Goal 

This project demonstrates the relationship between a pupil function, phase aberrations, and the focal-plane point spread function (PSF) in a simplified optical system.

In Fourier optics, the complex field across the pupil determines the focal-plane diffraction pattern. A perfect circular pupil produces a diffraction-limited PSF. Adding phase aberrations across the pupil changes the distribution of intensity in the focal plane

## Concepts Demonstrated

- Pupil function
- Circular aperture
- Complex optical field
- Wavefront phase
- Point spread function (PSF)
- Diffraction-limited imaging
- Defocus
- Astigmatism
- Coma
- Ideal phase correction
- Relationship between pupil-plane phase and focal-plane image quality

## Physical Interpretation

A pupil is the aperture stop of an optical system or an image of that aperture stop. It defines which portions of the optical wavefront pass through the system.

The pupil function describes the complex optical field across the pupil. In this simulation, the pupil function includes an amplitude term and a phase term:

```text
pupil field = aperture × exp(i × phase)

The PSF describes how an optical system images a point source. In this scalar Fourier-optics model, the focal-plane field is calculated from the Fourier transform of the complex pupil field, and the PSF is the squared magnitude of that field. 

```text
PSF = abs(Fourier transform of pupil field) ^ 2

A flat phase across a circular pupil produces a diffraction-limited Airy-like PSF. Aberrations introduce phase variation across the pupil, which redistributes energy in the focal plane and degrades image quality. 

## Aberrations Simulated

This script applied several simple phase aberrations across a circular pupil:

1. Diffraction-limited pupil with flat phase
2. Defocus aberration 
3. Astigmatism aberration
4. Coma aberration
5. Ideal phase correction of coma

# Defocus 

1. Defocus aberration 

Defocus introduces a radially symmetric quadratic phase variation across the pupil. It corresponds to observing the image awat from the best-focus plane. 

In the PSF, defocus spreads energy away from the central peak and can create broader ring-like structure. 

# Astigmatism 

Astigmatism introduces different phase curvature along two perpendicular axes. It corresponds to different effective focal positions in orthogonal directions

# Coma 

Coma introduces an asymmetric phase variation across the pupil. It is commonly associated with off-axis imaging. In the PSF, coma produces a lopsided, comet-like intensity pattern. 

# Ideal Phase Correction

An ideal corrective phase pattern applies the opposite phase of the aberration. In this simplified model, applying the opposite phase cancels the wavefront error and restores the diffraction-limited PSF. This is conceptually related to Adaptive Optics, where a deformable mirror or spatial light modulator can be used to compensate wavefront error. 

# Simulations

This script generates a circular pupil, applies different pupil-plane phase functions, and computes the corresponding focal-plane PSFs.

The simulation flow is:

Pupil amplitude & phase -> complex pupil field -> Fourier transform -> focal-plane intensity / PSF