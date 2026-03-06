import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# Gravitational constant
G = 6.67430e-11  # m^3 kg^-1 s^-2
SQRT_3_2 = np.sqrt( 3 ) / 2
NUM_1_2 = 0.5


def three_body( args ) :

    X_MIN=args.x_min
    X_MAX=args.x_max
    Y_MIN=args.y_min
    Y_MAX=args.y_max

    # Simulation parameters
    t_scale = args.t_scale
    dt = 0.001 / t_scale  # Smaller time step for stability (s)
    t_ini = args.t_ini
    t_max = t_ini * t_scale  # Longer simulation time for visible divergence (s)
    steps = int(t_max / dt)
    v_scale=args.v_scale
    x_scale=args.x_scale
    print( f"--> Parameters: t_ini={t_ini},t_scale={t_scale},x_scale={x_scale},v_scale={v_scale}" )


    # Body properties (Earth-like masses)
    masses = np.array([8.972e24, 5.972e24, 3.972e24])  # kg

    # Initial conditions for two scenarios
    # Scenario A: Base case
    # Scenario B: Perturb Body 3's position by 10 meters (increased for visibility)
    positions_a = [
        np.array([x_scale*0.0, x_scale*0.0]),          # Body 1 (m)
        np.array([x_scale*1.0e6, x_scale*0.0]),        # Body 2 (m)
        np.array([x_scale*0.5e6, x_scale*0.866e6])     # Body 3 (m, rough equilateral triangle)
    ]
    velocities_a = [
        np.array([v_scale*0.0, v_scale*100.0]),        # Body 1 (m/s)
        np.array([v_scale*0.0, v_scale*(-100.0)]),       # Body 2 (m/s)
        np.array([v_scale*(-86.6), v_scale*50.0])        # Body 3 (m/s)
    ]

    # Scenario B: Perturb Body 3's position
    positions_b = positions_a.copy()
    #positions_b[2] = np.array([0.5e6 + 10.0, 0.866e6])  # Perturbed by 10 m
    positions_b[2] = np.array([x_scale*0.5e6 + x_scale*10.0, x_scale*0.866e6])  # Perturbed by 10 m
    velocities_b = velocities_a.copy()

    # Arrays to store trajectories
    traj_a = np.zeros((steps, 3, 2))  # Trajectories for 3 bodies, Scenario A
    traj_b = np.zeros((steps, 3, 2))  # Trajectories for 3 bodies, Scenario B
    traj_a[0] = positions_a
    traj_b[0] = positions_b

    # Function to compute gravitational acceleration on one body
    def gravitational_acceleration(pos_i, pos_j, m_i, m_j):
        r = pos_j - pos_i
        r_norm = np.linalg.norm(r)
        if r_norm < 1e-10:  # Avoid division by zero
            return np.zeros(2)
        force_magnitude = G * m_i * m_j / r_norm**3
        return force_magnitude * r / m_i  # Acceleration on body i

    # Function to compute total acceleration for one body
    def total_acceleration(i, positions, masses):
        acc = np.zeros(2)
        for j in range(len(masses)):
            if i != j:
                acc += gravitational_acceleration(positions[i], positions[j], masses[i], masses[j])
        return acc

    # Velocity Verlet integration for better stability
    velocities_a_t = [v.copy() for v in velocities_a]
    velocities_b_t = [v.copy() for v in velocities_b]

    def calc_progress( t, steps ) :
        bar_size=100
        dashes = int( ( t / steps ) * 100.0 ) + 1
        spaces = bar_size - dashes
        return "".join( [ "-" ] ) * dashes + "".join( [ " " ] * spaces )

    for t in range(1, steps):
        progress = calc_progress( t, steps )
        print( f"[{progress}]", end="\r" )
        # Scenario A
        # Step 1: Compute accelerations at current positions
        acc_a = [total_acceleration(i, traj_a[t-1], masses) for i in range(3)]
        # Step 2: Update positions
        for i in range(3):
            traj_a[t, i] = traj_a[t-1, i] + velocities_a_t[i] * dt + 0.5 * acc_a[i] * dt**2
        # Step 3: Compute new accelerations
        acc_a_new = [total_acceleration(i, traj_a[t], masses) for i in range(3)]
        # Step 4: Update velocities
        for i in range(3):
            velocities_a_t[i] += 0.5 * (acc_a[i] + acc_a_new[i]) * dt

        # Scenario B
        acc_b = [total_acceleration(i, traj_b[t-1], masses) for i in range(3)]
        for i in range(3):
            traj_b[t, i] = traj_b[t-1, i] + velocities_b_t[i] * dt + 0.5 * acc_b[i] * dt**2
        acc_b_new = [total_acceleration(i, traj_b[t], masses) for i in range(3)]
        for i in range(3):
            velocities_b_t[i] += 0.5 * (acc_b[i] + acc_b_new[i]) * dt

    print( "\n--> Done!" )

    # Debug: Check if trajectories diverge
    print("Distance between Body 3 (A vs B) at final step:", np.linalg.norm(traj_a[-1, 2] - traj_b[-1, 2]))

    # Plotting
    plt.figure(figsize=(12, 8))
    #Y_MIN=-0.75e6
    #Y_MAX=1.25e6
    #X_MIN=-1e6
    #X_MAX=2e6

    # Colors for bodies
    colors = ['blue', 'red', 'green']
    labels = ['Body 1', 'Body 2', 'Body 3']

    # Scenario A (solid lines)
    for i in range(3):
        plt.plot(traj_a[:, i, 0], traj_a[:, i, 1], color=colors[i], linestyle='-', 
                 label=f'{labels[i]} (Scenario A)')

    # Scenario B (dashed lines)
    for i in range(3):
        plt.plot(traj_b[:, i, 0], traj_b[:, i, 1], color=colors[i], linestyle='--', 
                 label=f'{labels[i]} (Scenario B)')

    # Mark initial positions
    for i in range(3):
        plt.plot(traj_a[0, i, 0], traj_a[0, i, 1], 'o', color=colors[i], 
                 label=f'{labels[i]} Start (A)' if i == 0 else None)
        plt.plot(traj_b[0, i, 0], traj_b[0, i, 1], '*', color=colors[i], 
                 label=f'{labels[i]} Start (B)' if i == 2 else None)

    # Dynamically adjust axis limits
    all_x = np.concatenate([traj_a[:, :, 0].flatten(), traj_b[:, :, 0].flatten()])
    all_y = np.concatenate([traj_a[:, :, 1].flatten(), traj_b[:, :, 1].flatten()])
    #x_min, x_max = all_x.min(), all_x.max()
    #y_min, y_max = all_y.min(), all_y.max()
    #Y_MIN=-0.75e6
    #Y_MAX=1.25e6
    #X_MIN=-1e6
    #X_MAX=2e6
    #if x_min < X_MIN :
    #    x_min = X_MIN
    #if x_max > X_MAX :
    #    x_max = X_MAX 
    #if y_min < Y_MIN :
    #    y_min = Y_MIN
    #if y_max > Y_MAX :
    #    y_max = Y_MAX
    #plt.xlim(x_min - 0.1 * abs(x_min), x_max + 0.1 * abs(x_max))
    #plt.ylim(y_min - 0.1 * abs(y_min), y_max + 0.1 * abs(y_max))
    #plt.xlim(X_MIN, X_MAX)
    #plt.ylim(Y_MIN, Y_MAX)

    plt.title("Butterfly Effect in the 3-Body Problem")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.legend()
    plt.grid(True)
    #plt.axis('equal')
    plt.xlim(X_MIN, X_MAX)
    plt.ylim(Y_MIN, Y_MAX)
    if args.config is not None :
        return plt

    plt.savefig(f"graphs/n_body_problem/t_ini={t_ini},t_scale={t_scale},x_scale={x_scale},v_scale={v_scale}_window={X_MIN},{X_MAX},{Y_MIN},{Y_MAX}_n_body_problem.png", dpi=300, bbox_inches='tight')

def circle_with_velocity( args ) :
    X_MIN=args.x_min
    X_MAX=args.x_max
    Y_MIN=args.y_min
    Y_MAX=args.y_max

    # Simulation parameters
    t_scale = args.t_scale
    dt = 0.001 / t_scale  # Smaller time step for stability (s)
    t_ini = args.t_ini
    t_max = t_ini * t_scale  # Longer simulation time for visible divergence (s)
    steps = int(t_max / dt)
    v_scale=args.v_scale
    x_scale=args.x_scale
    print( f"--> Parameters: t_ini={t_ini},t_scale={t_scale},x_scale={x_scale},v_scale={v_scale}" )


    # Body properties (Earth-like masses)
    masses = np.array([8.972e24, 5.972e24, 3.972e24])  # kg
    velocities = np.array([100, 100, 100])
    R=1e6

    # Initial conditions for two scenarios
    # Scenario A: Base case
    # Scenario B: Perturb Body 3's position by 10 meters (increased for visibility)
    positions_a = [
        np.array([-x_scale*R*NUM_1_2,  x_scale*R*SQRT_3_2]),    # Body 1 (m)
        np.array([-x_scale*R*NUM_1_2, -x_scale*R*SQRT_3_2]),    # Body 2 (m)
        np.array([ x_scale*R,                           0])     # Body 3 (m, rough equilateral triangle)
    ]
    velocities_a = [
        np.array([-v_scale*velocities[0]*SQRT_3_2, -v_scale*velocities[0]*NUM_1_2]),  # Body 1 (m/s)
        np.array([ v_scale*velocities[1]*SQRT_3_2,  v_scale*velocities[1]*NUM_1_2]),  # Body 2 (m/s)
        np.array([                              0,  v_scale*velocities[2]])           # Body 3 (m/s)
    ]

    # Scenario B: Perturb Body 3's position
    positions_b = positions_a.copy()
    #positions_b[2] = np.array([0.5e6 + 10.0, 0.866e6])  # Perturbed by 10 m
    positions_b[2] = np.array([x_scale*positions_a[2][0] + x_scale*10.0, x_scale*positions_a[2][1]])  # Perturbed by 10 m
    velocities_b = velocities_a.copy()

    # Arrays to store trajectories
    traj_a = np.zeros((steps, 3, 2))  # Trajectories for 3 bodies, Scenario A
    traj_b = np.zeros((steps, 3, 2))  # Trajectories for 3 bodies, Scenario B
    traj_a[0] = positions_a
    traj_b[0] = positions_b

    # Function to compute gravitational acceleration on one body
    def gravitational_acceleration(pos_i, pos_j, m_i, m_j):
        r = pos_j - pos_i
        r_norm = np.linalg.norm(r)
        if r_norm < 1e-10:  # Avoid division by zero
            return np.zeros(2)
        force_magnitude = G * m_i * m_j / r_norm**3
        return force_magnitude * r / m_i  # Acceleration on body i

    # Function to compute total acceleration for one body
    def total_acceleration(i, positions, masses):
        acc = np.zeros(2)
        for j in range(len(masses)):
            if i != j:
                acc += gravitational_acceleration(positions[i], positions[j], masses[i], masses[j])
        return acc

    # Velocity Verlet integration for better stability
    velocities_a_t = [v.copy() for v in velocities_a]
    velocities_b_t = [v.copy() for v in velocities_b]

    def calc_progress( t, steps ) :
        bar_size=100
        dashes = int( ( t / steps ) * 100.0 ) + 1
        spaces = bar_size - dashes
        return "".join( [ "-" ] ) * dashes + "".join( [ " " ] * spaces )

    for t in range(1, steps):
        progress = calc_progress( t, steps )
        print( f"[{progress}]", end="\r" )
        # Scenario A
        # Step 1: Compute accelerations at current positions
        acc_a = [total_acceleration(i, traj_a[t-1], masses) for i in range(3)]
        # Step 2: Update positions
        for i in range(3):
            traj_a[t, i] = traj_a[t-1, i] + velocities_a_t[i] * dt + 0.5 * acc_a[i] * dt**2
        # Step 3: Compute new accelerations
        acc_a_new = [total_acceleration(i, traj_a[t], masses) for i in range(3)]
        # Step 4: Update velocities
        for i in range(3):
            velocities_a_t[i] += 0.5 * (acc_a[i] + acc_a_new[i]) * dt

        # Scenario B
        acc_b = [total_acceleration(i, traj_b[t-1], masses) for i in range(3)]
        for i in range(3):
            traj_b[t, i] = traj_b[t-1, i] + velocities_b_t[i] * dt + 0.5 * acc_b[i] * dt**2
        acc_b_new = [total_acceleration(i, traj_b[t], masses) for i in range(3)]
        for i in range(3):
            velocities_b_t[i] += 0.5 * (acc_b[i] + acc_b_new[i]) * dt

    print( "\n--> Done!" )

    # Debug: Check if trajectories diverge
    print("Distance between Body 3 (A vs B) at final step:", np.linalg.norm(traj_a[-1, 2] - traj_b[-1, 2]))

    # Plotting
    plt.figure(figsize=(12, 8))
    #Y_MIN=-0.75e6
    #Y_MAX=1.25e6
    #X_MIN=-1e6
    #X_MAX=2e6

    # Colors for bodies
    colors = ['blue', 'red', 'green']
    labels = ['Body 1', 'Body 2', 'Body 3']

    # Scenario A (solid lines)
    for i in range(3):
        plt.plot(traj_a[:, i, 0], traj_a[:, i, 1], color=colors[i], linestyle='-', 
                 label=f'{labels[i]} (Scenario A)')

    # Scenario B (dashed lines)
    for i in range(3):
        plt.plot(traj_b[:, i, 0], traj_b[:, i, 1], color=colors[i], linestyle='--', 
                 label=f'{labels[i]} (Scenario B)')

    # Mark initial positions
    for i in range(3):
        plt.plot(traj_a[0, i, 0], traj_a[0, i, 1], 'o', color=colors[i], 
                 label=f'{labels[i]} Start (A)' if i == 0 else None)
        plt.plot(traj_b[0, i, 0], traj_b[0, i, 1], '*', color=colors[i], 
                 label=f'{labels[i]} Start (B)' if i == 2 else None)

    # Dynamically adjust axis limits
    all_x = np.concatenate([traj_a[:, :, 0].flatten(), traj_b[:, :, 0].flatten()])
    all_y = np.concatenate([traj_a[:, :, 1].flatten(), traj_b[:, :, 1].flatten()])
    #x_min, x_max = all_x.min(), all_x.max()
    #y_min, y_max = all_y.min(), all_y.max()
    #Y_MIN=-0.75e6
    #Y_MAX=1.25e6
    #X_MIN=-1e6
    #X_MAX=2e6
    #if x_min < X_MIN :
    #    x_min = X_MIN
    #if x_max > X_MAX :
    #    x_max = X_MAX 
    #if y_min < Y_MIN :
    #    y_min = Y_MIN
    #if y_max > Y_MAX :
    #    y_max = Y_MAX
    #plt.xlim(x_min - 0.1 * abs(x_min), x_max + 0.1 * abs(x_max))
    #plt.ylim(y_min - 0.1 * abs(y_min), y_max + 0.1 * abs(y_max))
    #plt.xlim(X_MIN, X_MAX)
    #plt.ylim(Y_MIN, Y_MAX)

    plt.title("Butterfly Effect in the 3-Body Problem")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.legend()
    plt.grid(True)
    #plt.axis('equal')
    plt.xlim(X_MIN, X_MAX)
    plt.ylim(Y_MIN, Y_MAX)
    if args.config is not None :
        return plt

    plt.savefig(f"graphs/n_body_problem/circle_t_ini={t_ini},t_scale={t_scale},x_scale={x_scale},v_scale={v_scale}_window={X_MIN},{X_MAX},{Y_MIN},{Y_MAX}_n_body_problem.png", dpi=300, bbox_inches='tight')

if __name__ == "__main__" :
    import argparse
    parser = argparse.ArgumentParser(description="N-Body Problem Script")
    parser.add_argument( '--t_scale', type=float, default=1.0, help='t_scale')
    parser.add_argument( '--t_ini',   type=float, default=38.0, help='t_ini')
    parser.add_argument( '--v_scale', type=float, default=1.0, help='v_scale')
    parser.add_argument( '--x_scale', type=float, default=1.0, help='x_scale')
    parser.add_argument( '--x_min',   type=float, default=-1e6, help='x_scale')
    parser.add_argument( '--x_max',   type=float, default=2e6, help='x_scale')
    parser.add_argument( '--y_min',   type=float, default=-0.75e6, help='x_scale')
    parser.add_argument( '--y_max',   type=float, default=1.25e6, help='x_scale')
    parser.add_argument( '--config',  type=str,   default=None, help='config file')
    args = parser.parse_args()

    if args.config is not None :
        three_body( args )

    circle_with_velocity( args )
