# Pupil Function, PSF, and Aberration Simulation

## Goal 

This project demonstrates the relationship between a pupil function, phase aberrations, and the focal-plane point spread function in a simplified optical system.

In Fourier optics, the complex field across the pupil determines the focal-plane diffraction pattern. A perfect circular pupil produces a diffraction-limited PSF. Adding phase aberrations across the pupil changes the distribution of intensity in the focal plane






This project demonstrates the relationship between a pupil function, phase aberrations, and the focal-plane point spread function in a simplified optical system.

In Fourier optics, the complex field across the pupil determines the focal-plane diffraction pattern. A perfect circular pupil produces a diffraction-limited PSF. Adding phase aberrations across the pupil changes the distribution of intensity in the focal plane.

## Concepts Demonstrated

- Pupil function
- Circular aperture
- Complex optical field
- Wavefront phase
- Point spread function
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