# src/mandelbrot_logistic.py
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

def logistic_map(x0, r, n, transient=500):
    x = x0
    for _ in range(transient):
        x = r * x * (1 - x)
    values = []
    for _ in range(n):
        x = r * x * (1 - x)
        values.append(x)
    return values


def mandelbrot_sequence(c, n, transient=500):
    z = 0.0 + 0j
    for _ in range(transient):
        z = z*z + c
        if abs(z) > 2:
            return []
    values = []
    for _ in range(n):
        z = z*z + c
        if abs(z) > 2:
            return []
        values.append(z.real)
    # Try to find near-periodic orbit in the end
    unique = []
    seen = set()
    for v in values[-60:]:
        vr = round(v, 6)
        if vr not in seen:
            seen.add(vr)
            unique.append(v)
    return unique if unique else values[-12:]


def plot_logistic_mandelbrot_bifurcation():
    r_min, r_max = 2.5, 4.0
    c_min, c_max = -1.90, -0.11
    n_points = 1200
    n_iter   = 220
    transient = 600

    # Logistic
    r_values = np.linspace(r_min, r_max, n_points)
    logistic_data = []
    for r in r_values:
        xs = logistic_map(0.5, r, n_iter, transient)
        logistic_data.extend([(r, x) for x in xs])

    # Mandelbrot real axis
    c_values = np.linspace(c_min, c_max, int(n_points * 2.4))
    mandel_data = []
    for c in c_values:
        zs = mandelbrot_sequence(c, n_iter, transient)
        mandel_data.extend([(c, z) for z in zs])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 13), sharex=False)

    # Logistic bifurcation
    rx, ry = zip(*logistic_data)
    ax1.scatter(rx, ry, s=0.015, color='black', alpha=0.6, rasterized=True)
    ax1.set_title("Logistic Map Bifurcation Diagram", fontsize=14)
    ax1.set_xlabel("r", fontsize=11)
    ax1.set_ylabel("x", fontsize=11)
    ax1.set_xlim(r_min, r_max)

    # Mandelbrot real slice
    if mandel_data:
        cx, cz = zip(*mandel_data)
        ax2.scatter(cx, cz, s=0.015, color='black', alpha=0.6, rasterized=True)
    ax2.set_title("Mandelbrot Set – Real Axis Orbit Bifurcation", fontsize=14)
    ax2.set_xlabel("Re(c)", fontsize=11)
    ax2.set_ylabel("Re(z)", fontsize=11)
    ax2.set_xlim(c_min, c_max)
    ax2.set_ylim(-2.1, 2.1)
    ax2.invert_yaxis()   # common convention for this view

    # Some annotation lines
    key_points = [
        (3.000, -0.75),
        (3.449, -1.25),
        (3.544, -1.363),
        (3.564, -1.391),
    ]
    for r, c in key_points:
        ax1.axvline(r, color='red', ls='--', lw=0.6, alpha=0.7)
        ax2.axvline(c, color='red', ls='--', lw=0.6, alpha=0.7)

    plt.tight_layout()
    out = Path("graphs/logistic_mandelbrot_bifurcation.png")
    out.parent.mkdir(exist_ok=True)
    plt.savefig(out, dpi=320, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")
