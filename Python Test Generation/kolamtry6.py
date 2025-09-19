import matplotlib.pyplot as plt
import numpy as np

# Set up the plot
plt.figure(figsize=(6, 6), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')
plt.axis('equal')
plt.axis('off')

# Dot positions for a 5x5 diamond grid
dot_coords = []
n = 5
for i in range(n):
    for j in range(n):
        if abs(i - 2) + abs(j - 2) <= 2:
            dot_coords.append((j, n-1-i))

# Draw the dots
for (x, y) in dot_coords:
    dot = plt.Circle((x, y), 0.08, color='white', fill=True)
    ax.add_patch(dot)

# Define the kolam path (manually traced for this pattern)
path = [
    (0,2), (1,3), (2,4), (3,3), (4,2), (3,1), (2,0), (1,1), (0,2), # Outer loop
    (1,2), (2,3), (3,2), (2,1), (1,2) # Inner loop
]

# Draw the outer loop
outer_x = [p[0] for p in path]
outer_y = [p[1] for p in path]
plt.plot(outer_x, outer_y, color='white', linewidth=2)

# Draw the inner diamonds (manually traced)
inner_paths = [
    [(1,2), (2,1), (3,2), (2,3), (1,2)]
]

for ipath in inner_paths:
    x = [p[0] for p in ipath]
    y = [p[1] for p in ipath]
    plt.plot(x, y, color='white', linewidth=2)

plt.show()