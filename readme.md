# 🌐 StereoProj-Viz: Interactive Manifold Projection

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-11557c?style=flat-square&logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Math](https://img.shields.io/badge/Topic-Riemannian%20Geometry-red?style=flat-square)](https://en.wikipedia.org/wiki/Riemannian_geometry)

> **Visualizing the bijection between Euclidean Space ($\mathbb{R}^2$) and the Riemann Sphere ($S^2$).**

This educational tool provides an interactive 3D visualization of the **Inverse Stereographic Transform**. It is designed to demonstrate how probability densities are mapped from a flat plane to a curved manifold, a core concept in **Riemannian Normalizing Flows**.

![Visualization Demo](demo.png)

## 🎯 Motivation

In geometric deep learning (e.g., *Normalizing Flows on Riemannian Manifolds*), we often map complex distributions from a flat space to a curved surface.

Understanding this mapping requires grasping two concepts:
1.  **Bijectivity:** Every point on the plane corresponds to a unique point on the sphere.
2.  **Volume Distortion:** The mapping is not isometric. Points far from the origin on the plane are "squashed" when mapped near the North Pole of the sphere. This distortion must be corrected using the **Jacobian Determinant**.

**StereoProj-Viz** allows you to "poke" the manifold and see the projection ray in real-time.

## ✨ Features

* **Interactive Picking:** Click on any **Red Point** (Sphere $S^2$) to visualize its connection to the **Blue Plane** ($\mathbb{R}^2$).
* **Ray Tracing:** Dynamically draws the projection line from the North Pole, through the Sphere, to the Plane.
* **Density Correction Info:** Real-time calculation of the **Jacobian Factor** (stretch factor), showing why density correction formulas (like $\sqrt{\det G}$) are necessary for probability conservation.
* **Visualizing Distortion:**
    * *South Pole (Origin):* Low distortion, ray is vertical.
    * *North Pole (Infinity):* High distortion, ray is highly oblique.

## 🧮 Mathematical Background

The tool visualizes the map $\phi: \mathbb{R}^n \to S^n$. For a point $u \in \mathbb{R}^2$, the corresponding point $x \in S^2$ is given by:

$$x = \frac{2u}{||u||^2 + 1}, \quad y = \frac{2v}{||u||^2 + 1}, \quad z = \frac{||u||^2 - 1}{||u||^2 + 1}$$

The **Jacobian Determinant** (area change) displayed in the console follows the metric:

$$\sqrt{\det G} \propto \left( \frac{2}{||u||^2 + 1} \right)^n$$

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* `numpy`
* `matplotlib`

```bash
pip install numpy matplotlib