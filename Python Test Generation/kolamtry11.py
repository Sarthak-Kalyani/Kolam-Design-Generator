import matplotlib.pyplot as plt
import numpy as np

grid_size = 6   # Use 6 for direct match, change as needed
spacing = 1.5
fig, ax = plt.subplots(figsize=(7,7))

# Draw grid dots
for i in range(grid_size):
    for j in range(grid_size):
        ax.plot(j * spacing, i * spacing, 'ko', markersize=6)

t = np.linspace(0, 2*np.pi, 100)

# Draw 'infinity' loops for each grid cell (between four dots)
for i in range(grid_size-1):
    for j in range(grid_size-1):
        cx = (j+0.5)*spacing
        cy = (i+0.5)*spacing
        r = spacing * 0.4
        # Infinity-shape: horizontal
        x = cx + r*np.cos(t)
        y = cy + r*np.sin(t) * np.cos(t)
        ax.plot(x, y, 'k', linewidth=1)

# Draw diagonal loops passing through cell centers
for i in range(grid_size-1):
    for j in range(grid_size-1):
        cx = (j+0.5)*spacing
        cy = (i+0.5)*spacing
        # Diagonal 1: Top-left to bottom-right
        x1 = np.linspace(j*spacing, (j+1)*spacing, 100)
        y1 = np.linspace(i*spacing, (i+1)*spacing, 100)
        ax.plot(x1, y1, 'k', linewidth=1)
        # Diagonal 2: Bottom-left to top-right
        x2 = np.linspace(j*spacing, (j+1)*spacing, 100)
        y2 = np.linspace((i+1)*spacing, i*spacing, 100)
        ax.plot(x2, y2, 'k', linewidth=1)

ax.set_aspect('equal')
plt.axis('off')
plt.show()
