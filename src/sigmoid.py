import numpy as np
import matplotlib.pyplot as plt

k = 1.0  # Rate constant
t = np.linspace(-5, 5, 100)
S = 1 / (1 + np.exp(-k * t))
S1 = 1 / (1 + np.exp(-2*k * t))
S2 = 1 / (1 + np.exp(-5*k * t))

plt.plot(t, S, label='k=1', color="red")
plt.plot(t, S1, label='k=2', color="orange")
plt.plot(t, S2, label='k=5', color="blue")
plt.title('Emergence of Order (Sigmoid Curve)')
plt.xlabel('Time (t)')
plt.ylabel('Order (S)')
plt.grid(True)
plt.legend()
plt.savefig("graphs/sigmoid.png", dpi=300, bbox_inches='tight')
