# src/cellular.py
try:
    import cellpylib as cpl
    CELL_PY_LIB_AVAILABLE = True
except ImportError:
    CELL_PY_LIB_AVAILABLE = False

import matplotlib.pyplot as plt
from pathlib import Path


def run_elementary_cellular_automata(rules=range(101, 111), size=200, steps=100):
    if not CELL_PY_LIB_AVAILABLE:
        print("cellpylib not installed → skipping cellular automata")
        print("Install with:  pip install cellpylib")
        return

    outdir = Path("graphs/cellular_automata")
    outdir.mkdir(parents=True, exist_ok=True)

    for rule in rules:
        print(f"Rule {rule:3d} ... ", end="", flush=True)
        ca = cpl.init_simple(size)
        ca = cpl.evolve(ca, timesteps=steps, apply_rule=lambda n,c,t: cpl.nks_rule(n, rule))
        cpl.plot(ca, show=False)
        plt.title(f"Elementary CA – Rule {rule}", fontsize=13)
        plt.savefig(outdir / f"rule_{rule:03d}.png", dpi=180, bbox_inches='tight')
        plt.close()
        print("done")
