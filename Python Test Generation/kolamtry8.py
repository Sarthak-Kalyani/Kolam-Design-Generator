import matplotlib.pyplot as plt
import numpy as np

# Draw a single dot
def draw_dot(x, y, r=0.08, color='saddlebrown'):
    dot = plt.Circle((x, y), r, color=color, fill=True, zorder=3)
    plt.gca().add_patch(dot)

# Draw a circle around a dot
def draw_circle(x, y, r=0.35, color='saddlebrown'):
    circ = plt.Circle((x, y), r, color=color, fill=False, linewidth=2, zorder=2)
    plt.gca().add_patch(circ)

# Draw a cross at a dot
def draw_cross(x, y, size=0.7, color='saddlebrown'):
    plt.plot([x - size, x + size], [y, y], color=color, linewidth=2, zorder=2)
    plt.plot([x, x], [y - size, y + size], color=color, linewidth=2, zorder=2)

# Draw a loop around a dot
def draw_loop(x, y, dx, dy, size=0.7, color='saddlebrown'):
    # Loop direction defined by (dx, dy)
    t = np.linspace(0, np.pi, 100)
    r = size
    x1 = x + dx * 0.5
    y1 = y + dy * 0.5

    if dx == 0:  # Vertical loop
        xs = x + r * np.cos(t)
        ys = y1 + dy * r * np.sin(t)
    else:  # Horizontal loop
        xs = x1 + dx * r * np.sin(t)
        ys = y + r * np.cos(t)

    plt.plot(xs, ys, color=color, linewidth=2, zorder=2)

# Draw grid with selected pattern
def draw_grid(k, l, pattern_type=0):
    plt.figure(figsize=(2.5, 2.5), facecolor='#f5e6d3')
    plt.gca().set_facecolor('#f5e6d3')
    plt.axis('equal')
    plt.axis('off')

    n = k + l + 1
    dots = []

    # Place dots
    for i in range(n):
        for j in range(n):
            dots.append((j, n - 1 - i))
            draw_dot(j, n - 1 - i)

    # Draw patterns
    if pattern_type == 0:  # Crosses
        for (x, y) in dots:
            draw_cross(x, y)
    elif pattern_type == 1:  # Circles
        for (x, y) in dots:
            draw_circle(x, y)
    elif pattern_type == 2:  # Loops
        for (x, y) in dots:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in dots:
                    draw_loop(x, y, dx, dy)

    plt.xlim(-1, n)
    plt.ylim(-1, n)
    plt.tight_layout()
    plt.show()

# Example usage:
draw_grid(1, 1, pattern_type=0)  # Cross pattern
draw_grid(1, 1, pattern_type=1)  # Circle pattern
draw_grid(2, 2, pattern_type=2)  # Loop pattern
draw_grid(3, 3, pattern_type=0)  # Cross pattern
draw_grid(3, 3, pattern_type=1)  # Circle pattern
draw_grid(3, 3, pattern_type=2)  # Loop pattern
