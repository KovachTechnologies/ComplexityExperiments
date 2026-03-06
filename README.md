# Chaos, Fractals & Complexity Experiments

A collection of classic demonstrations and visualizations from **nonlinear dynamics**, **chaos theory**, **fractals** and **complex systems**.

This repository contains clean, modular Python implementations of several iconic systems and phenomena frequently discussed in complexity science, popular science books (e.g. *Chaos* by James Gleick, *Sync* by Steven Strogatz), and introductory courses on dynamical systems.

## Included Experiments

| Experiment                        | File                          | What it shows / demonstrates                              |
|-------------------------------|-------------------------------|------------------------------------------------------------------|
| Lorenz attractor (1963)        | `src/lorenz.py`               | Classic strange attractor, sensitive dependence on initial conditions |
| Sigmoid / logistic growth     | `src/sigmoid.py`              | Emergence of order, phase transition-like behavior               |
| Three-body problem            | `src/threebody.py`            | Butterfly effect & chaos in Newtonian gravity (very long-term divergence) |
| Logistic map bifurcation      | `src/mandelbrot_logistic.py`  | Period-doubling cascade, onset of chaos                         |
| Real-axis Mandelbrot orbits   | `src/mandelbrot_logistic.py`  | Connection between logistic map and Mandelbrot set along real line |
| Elementary cellular automata  | `src/cellular.py`             | Wolfram's elementary rules (mostly 101–110), self-organization patterns |

## Features

- Unified command-line interface (`main.py`)
- High-resolution output plots saved to `graphs/`
- Clean modular structure — easy to extend with new systems
- Minimal dependencies

## Requirements

Python 3.9 – 3.12 recommended

```text
numpy
matplotlib
scipy
pandas
cellpylib               # only needed for cellular automata
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

or minimally:

```bash
pip install numpy matplotlib scipy pandas cellpylib
```

## Installation

```bash
# 1. Clone or download the repository
git clone https://github.com/YOUR-USERNAME/chaos-fractals-experiments.git
cd chaos-fractals-experiments

# 2. (recommended) create virtual environment
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# or on Windows:  .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

All experiments are launched through the main script:

```bash
python main.py --experiment <name>
```

Available experiments:

```text
lorenz              Lorenz strange attractor (3D)
sigmoid             Family of sigmoid curves (emergence / order)
threebody           3-body gravitational problem — butterfly effect demo
mandel-logistic     Logistic map bifurcation + real-axis Mandelbrot orbits
cellular            Elementary cellular automata (default: rules 101–110)
all                 Run every experiment one after another
```

### Examples

```bash
# Classic Lorenz attractor
python main.py --experiment lorenz

# Three-body chaos demonstration
python main.py --experiment threebody --t-scale 2.5 --t-ini 45

# Logistic ↔ Mandelbrot connection
python main.py --experiment mandel-logistic

# Generate cellular automata rules 90, 110, 30, 184
python main.py --experiment cellular --ca-rules 30 90 110 184

# Everything (takes longest)
python main.py --experiment all
```

All generated images are saved in the `graphs/` folder (subfolders are created automatically where needed).

## Directory Structure

```text
chaos-fractals-experiments/
├── main.py                     ← command-line entry point
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── lorenz.py
│   ├── sigmoid.py
│   ├── threebody.py
│   ├── mandelbrot_logistic.py
│   └── cellular.py
├── graphs/                     ← output folder (gitignored by default)
└── README.md
```

## License

MIT License

Copyright (c) 2025 quantguy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Feel free to open issues or pull requests if you would like to:

- add new systems (Rössler attractor, Hénon map, Julia sets, boids, …)
- improve plot styling / interactivity
- add parameter sweeps / animations
- include Lyapunov exponent calculations
- add 2D Mandelbrot renderer

Enjoy exploring chaos & complexity!
