#!/usr/bin/env python3
"""
Chaos, Fractals & Complexity Experiments
"""

import argparse
import sys
from pathlib import Path

# Import your modules
from src.lorenz           import plot_lorenz_attractor
from src.sigmoid          import plot_sigmoid_curves
from src.threebody        import run_three_body_simulation
from src.mandelbrot_logistic import plot_logistic_mandelbrot_bifurcation
from src.cellular         import run_elementary_cellular_automata


def main():
    parser = argparse.ArgumentParser(description="Chaos, Fractals & Complexity Experiments")
    parser.add_argument("--experiment", "-e", required=True,
                        choices=[
                            "lorenz", "sigmoid", "threebody",
                            "mandel-logistic", "cellular",
                            "all"
                        ],
                        help="Which experiment to run")
    
    # Optional parameters for threebody
    parser.add_argument("--t-scale",   type=float, default=1.0)
    parser.add_argument("--t-ini",     type=float, default=38.0)
    parser.add_argument("--v-scale",   type=float, default=1.0)
    parser.add_argument("--x-scale",   type=float, default=1.0)

    # Optional for cellular automata
    parser.add_argument("--ca-rules",  nargs="+", type=int, default=range(101,111),
                        help="Elementary CA rules to generate (default: 101–110)")

    args = parser.parse_args()

    graphs_dir = Path("graphs")
    graphs_dir.mkdir(exist_ok=True)

    match args.experiment:
        case "lorenz":
            plot_lorenz_attractor()

        case "sigmoid":
            plot_sigmoid_curves()

        case "threebody":
            run_three_body_simulation(
                t_scale = args.t_scale,
                t_ini   = args.t_ini,
                v_scale = args.v_scale,
                x_scale = args.x_scale,
            )

        case "mandel-logistic":
            plot_logistic_mandelbrot_bifurcation()

        case "cellular":
            run_elementary_cellular_automata(rules=args.ca_rules)

        case "all":
            print("Running all experiments (this may take a while)...")
            plot_lorenz_attractor()
            plot_sigmoid_curves()
            run_three_body_simulation()
            plot_logistic_mandelbrot_bifurcation()
            run_elementary_cellular_automata()

        case _:
            parser.print_help()
            sys.exit(1)

    print(f"\nDone. Plots saved in: {graphs_dir.resolve()}")


if __name__ == "__main__":
    main()
