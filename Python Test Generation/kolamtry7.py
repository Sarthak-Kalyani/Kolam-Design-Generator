import matplotlib.pyplot as plt
import numpy as np

# Function to draw a dot
def draw_dot(x, y, r=0.08):
    dot = plt.Circle((x, y), r, color='white', fill=True, zorder=3)
    plt.gca().add_patch(dot)

# Set up the plot
plt.figure(figsize=(6, 6), facecolor='black')
plt.gca().set_facecolor('black')
plt.axis('equal')
plt.axis('off')

# Diamond grid dot positions (5x5 diamond)
dot_positions = [
    (2, 4),
    (1, 3), (2, 3), (3, 3),
    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
    (1, 1), (2, 1), (3, 1),
    (2, 0)
]

# Draw dots
for x, y in dot_positions:
    draw_dot(x, y)

# Draw the kolam loops (manually traced for this pattern)
# Each loop is a parametric curve around each dot
def draw_loop(cx, cy, size=0.9):
    t = np.linspace(0, 2*np.pi, 200)
    x = cx + size * np.cos(t) * np.abs(np.cos(t))
    y = cy + size * np.sin(t) * np.abs(np.sin(t))
    plt.plot(x, y, color='white', linewidth=2, zorder=2)

# Outer loops
outer_loops = [
    (2, 4), (1, 3), (3, 3), (0, 2), (4, 2), (1, 1), (3, 1), (2, 0)
]
for cx, cy in outer_loops:
    draw_loop(cx, cy, size=0.7)

# Inner loops
inner_loops = [
    (2, 3), (1, 2), (3, 2), (2, 1), (2, 2)
]
for cx, cy in inner_loops:
    draw_loop(cx, cy, size=0.45)

plt.show()