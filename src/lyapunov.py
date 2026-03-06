import numpy as np
import matplotlib.pyplot as plt
import os

def logistic_map(x, r):
    """Logistic map function: f(x) = r * x * (1 - x)"""
    return r * x * (1 - x)

def logistic_derivative(x, r):
    """Derivative of the logistic map: f'(x) = r * (1 - 2x)"""
    return r * (1 - 2 * x)

def compute_lyapunov_exponent(r, x0=0.5, n_transient=1000, n_iterations=1000):
    """Calculate the Lyapunov exponent for the logistic map."""
    x = x0
    for _ in range(n_transient):
        x = logistic_map(x, r)
    
    lyap_sum = 0.0
    for _ in range(n_iterations):
        derivative = logistic_derivative(x, r)
        lyap_sum += np.log(abs(derivative))
        x = logistic_map(x, r)
    
    return lyap_sum / n_iterations

def compute_bifurcation_data(r_values, x0=0.5, n_transient=1000, n_iterations=100):
    """Compute points for the bifurcation diagram."""
    bifurcation_data = []
    for r in r_values:
        x = x0
        # Transient iterations to reach steady state
        for _ in range(n_transient):
            x = logistic_map(x, r)
        # Collect points after transient
        for _ in range(n_iterations):
            x = logistic_map(x, r)
            bifurcation_data.append((r, x))
    return bifurcation_data

def plot_logistic_and_lyapunov(x0=0.5, r_min=2.5, r_max=4.0, n_r_points=50000, n_transient=2000, n_iterations=2000):
    """Plot the bifurcation diagram above the Lyapunov exponent."""
    r_values = np.linspace(r_min, r_max, n_r_points)
    
    # Compute Lyapunov exponent
    lyap_values = [compute_lyapunov_exponent(r, x0, n_transient, n_iterations) for r in r_values]
    
    # Compute bifurcation data
    bifurcation_data = compute_bifurcation_data(r_values, x0, n_transient, 500)  # Fewer iterations for density
    
    # Create two-panel figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, height_ratios=[1, 1])
    
    # Top plot: Bifurcation diagram (scatter plot)
    r_data, x_data = zip(*bifurcation_data)
    ax1.plot(r_data, x_data, 'k,', lw=0.1, markersize=0.2 )  # Blue points, dense scatter
    ax1.set_title(f"Logistic Map Bifurcation (x0={x0})", fontsize=14, loc='center')
    ax1.set_ylabel("x", fontsize=12)
    ax1.ticklabel_format(style='plain')
    
    # Bottom plot: Lyapunov exponent (line plot)
    ax2.plot(r_values, lyap_values, 'b')  # Blue line
    ax2.axhline(0, color='k', linestyle='--', lw=0.5)  # Zero line
    ax2.set_title(f"Lyapunov Exponent (x0={x0}, n={n_iterations})", fontsize=14, loc='center')
    ax2.set_xlabel("r", fontsize=12)
    ax2.set_ylabel("Lyapunov Exponent (λ)", fontsize=12)
    ax2.ticklabel_format(style='plain')
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Ensure graphs folder exists
    os.makedirs("graphs", exist_ok=True)
    
    # Save plot
    output_filename = f"logistic_and_lyapunov_x0={x0}_r={r_min}-{r_max}_n={n_iterations}.png"
    output_filepath = os.path.join("graphs", output_filename)
    plt.savefig(output_filepath, dpi=300)
    plt.close()
    print(f"Saved plot to {output_filepath}")

# Run the plot
if __name__ == "__main__":
    plot_logistic_and_lyapunov(x0=0.5, r_min=2.5, r_max=4.0, n_r_points=1000, n_transient=1000, n_iterations=1000)
