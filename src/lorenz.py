#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection  # Correct import

def lorenz_attractor(sigma=10.0, rho=28.0, beta=8.0/3.0, dt=0.01, num_steps=10000, x0=0.1, y0=0.0, z0=0.0):
    """
    Compute the Lorenz Attractor trajectory.
    Parameters: sigma, rho, beta (system parameters), dt (time step), num_steps, initial conditions (x0, y0, z0).
    Returns: x, y, z arrays of the trajectory.
    """
    x = np.zeros(num_steps)
    y = np.zeros(num_steps)
    z = np.zeros(num_steps)
    
    # Set initial conditions
    x[0], y[0], z[0] = x0, y0, z0
    
    # Iterate using the Lorenz equations
    for i in range(num_steps - 1):
        x[i + 1] = x[i] + dt * sigma * (y[i] - x[i])
        y[i + 1] = y[i] + dt * (x[i] * (rho - z[i]) - y[i])
        z[i + 1] = z[i] + dt * (x[i] * y[i] - beta * z[i])
    
    return x, y, z

def plot_lorenz_attractor():
    # Generate the Lorenz Attractor data
    x, y, z = lorenz_attractor()
    
    # Create a 3D plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the trajectory with a grayscale colormap
    points = np.array([x, y, z]).T
    segments = np.concatenate([points[:-1, np.newaxis], points[1:, np.newaxis]], axis=1)
    norm = plt.Normalize(0, len(x))
    lc = Line3DCollection(segments, cmap='gray', norm=norm)
    lc.set_array(np.linspace(0, 1, len(x)))
    ax.add_collection3d(lc)
    
    # Set axis limits
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_zlim(min(z), max(z))
    
    # Match styling from your code
    ax.set_xlabel('X', fontsize=6)
    ax.set_ylabel('Y', fontsize=6)
    ax.set_zlabel('Z', fontsize=6)
    ax.tick_params(axis='both', which='major', labelsize=4)
    ax.tick_params(axis='both', which='minor', labelsize=4)
    ax.set_title('Lorenz Attractor', fontsize=14, loc='center')
    
    # Save the plot
    plt.savefig("graphs/lorenz_attractor.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    # Ensure the output directory exists
    import os
    os.makedirs("graphs", exist_ok=True)
    
    # Generate and plot the Lorenz Attractor
    plot_lorenz_attractor()
