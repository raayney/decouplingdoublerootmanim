# 3D Boundary Fiber Geometry & Parameter Trajectory Visualizer

[![Manim](https://img.shields.io/badge/Rendered%20with-Manim%20Community-v0.18.0-blue?logo=python)](https://www.manim.community/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A 3D mathematical animation built with **Manim** to visualize the deformation of a complex fiber surface under a continuous parameter shift $\lambda(t) \in \mathbb{C}$.

The scene simultaneously renders the evolution of the symbol space parameter along the diagonal ray $\lambda(t) = t(1+i)$ and the corresponding geometric deformation of the 3D boundary fiber surface.

---

## Math & Mathematical Formulation

### 1. Symbol Space Trajectory (Left Panel)
The parameter $\lambda \in \mathbb{C}$ moves along a linear ray in the first quadrant of the complex plane:
$$\lambda(t) = t + i t, \quad t \in [0, 5.0]$$

### 2. Fiber Surface Mapping (Right Panel)
The surface is generated over a punctured polar domain centered at $b_0 = 1$ in the complex plane $b \in \mathbb{C}$:
$$b(r, \theta) = (1 + r\cos\theta) + i (r\sin\theta), \quad r \in [0.15, 0.7], \; \theta \in [0, 2\pi)$$

For each value of $\lambda(t)$, points on the base $b$-plane map to the rational function:
$$d(b, \lambda) = \frac{1 - b}{2 \lambda b^2}$$

### 3. Geometric Embedding & Color Encoding
The 3D visualization maps complex values into a 4-dimensional representation $(X, Y, Z, \text{Color})$:
* **Spatial Coordinates $(X, Y, Z)$:**
  $$X = \operatorname{Re}(b), \quad Y = \operatorname{Im}(b), \quad Z = \operatorname{Re}(d)$$
* **Color Gradient:** The face color of each surface quadrilateral dynamically interpolates from $\text{TEAL}$ to $\text{RED}$ based on $\operatorname{Im}(d) \in [-1.5, 1.5]$.

---

## Scene Architecture

```text
                               Scene1RootShiftTrajectory
                                          │
                     ┌────────────────────┴────────────────────┐
                     ▼                                         ▼
         Left: ComplexPlane (2D)                    Right: ThreeDAxes (3D)
    ──────────────────────────────────        ─────────────────────────────────
    • Trajectory: λ(t) = t(1 + i)             • Surface: b = 1 + r*e^(iθ)
    • ValueTracker: t ∈ [0.0, 5.0]            • Z-Axis: Re(d)
    • Always-redrawn indicator                • Color Map: Im(d) (Teal → Red)
```

---

## Quick Start

### Prerequisites
* **Python 3.9+**
* **Manim Community Edition**
* **FFmpeg** & **System LaTeX** (for math rendering)

### Installation
```bash
git clone https://github.com/your-username/fiber-geometry-manim.git
cd fiber-geometry-manim
pip install manim numpy
```

### Rendering the Scene

#### Low Resolution (Fast Preview)
```bash
manim -pql scene.py Scene1RootShiftTrajectory
```

#### High Quality (1080p, 60 FPS)
```bash
manim -pqh scene.py Scene1RootShiftTrajectory
```

#### 4K Resolution
```bash
manim -pqk scene.py Scene1RootShiftTrajectory
```

---

## File Structure

```text
.
├── scene.py                 # Main Manim script (Scene1RootShiftTrajectory)
├── README.md                # Documentation & Mathematical overview
└── media/                   # Rendered output videos and images
```

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
