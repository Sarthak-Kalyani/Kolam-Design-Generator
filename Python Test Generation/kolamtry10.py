import matplotlib.pyplot as plt
import numpy as np

grid_size = 6
spacing = 1.5
fig, ax = plt.subplots(figsize=(7,7))

# Draw dots
for i in range(grid_size):
    for j in range(grid_size):
        ax.plot(j*spacing, i*spacing, 'ko', markersize=7)

t = np.linspace(0, np.pi, 100)
# Diagonal curves (top-left to bottom-right and vice versa)
for i in range(grid_size-1):
    for j in range(grid_size-1):
        x0 = j*spacing
        y0 = i*spacing
        x1 = (j+1)*spacing
        y1 = (i+1)*spacing
        # Diagonal 1
        ax.plot(
            x0 + (x1-x0)*t/np.pi + spacing/4*np.sin(t),
            y0 + (y1-y0)*t/np.pi + spacing/4*np.sin(t),
            'k', linewidth=1)
        # Diagonal 2 (top-right to bottom-left)
        ax.plot(
            x1 - (x1-x0)*t/np.pi - spacing/4*np.sin(t),
            y0 + (y1-y0)*t/np.pi + spacing/4*np.sin(t),
            'k', linewidth=1)

# Figure-8 loops as before
t2 = np.linspace(0, 2*np.pi, 100)
for i in range(grid_size-1):
    for j in range(grid_size-1):
        cx = (j+0.5)*spacing
        cy = (i+0.5)*spacing
        x = cx + (spacing/2)*np.cos(t2)
        y = cy + (spacing/2)*np.sin(t2) * np.cos(t2)
        ax.plot(x, y, 'k', linewidth=1)

ax.set_aspect('equal')
plt.axis('off')
plt.show()
