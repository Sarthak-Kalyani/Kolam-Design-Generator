import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
import random

def draw_curve(ax, x, y, rule, r=0.5):
    if rule == 0:  # empty
        return
    elif rule == 1:  # full loop around dot
        ax.add_patch(Circle((x, y), r, fill=False, color='black', lw=1))
    elif rule == 2:  # horizontal ∞ shape (two side arcs)
        ax.add_patch(Arc((x-r/2, y), r, r, angle=0, theta1=-90, theta2=90, lw=1))
        ax.add_patch(Arc((x+r/2, y), r, r, angle=0, theta1=90, theta2=270, lw=1))
    elif rule == 3:  # vertical ∞ shape (two vertical arcs)
        ax.add_patch(Arc((x, y-r/2), r, r, angle=0, theta1=0, theta2=180, lw=1))
        ax.add_patch(Arc((x, y+r/2), r, r, angle=0, theta1=180, theta2=360, lw=1))
    elif rule == 4:  # diagonal cross arcs
        ax.add_patch(Arc((x-r/2, y-r/2), r, r, angle=0, theta1=0, theta2=90, lw=1))
        ax.add_patch(Arc((x+r/2, y+r/2), r, r, angle=0, theta1=180, theta2=270, lw=1))
        ax.add_patch(Arc((x-r/2, y+r/2), r, r, angle=0, theta1=270, theta2=360, lw=1))
        ax.add_patch(Arc((x+r/2, y-r/2), r, r, angle=0, theta1=90, theta2=180, lw=1))
    elif rule == 5:  # diamond/square loop
        ax.add_patch(Arc((x-r/2, y), r, r, angle=0, theta1=-90, theta2=90, lw=1))
        ax.add_patch(Arc((x+r/2, y), r, r, angle=0, theta1=90, theta2=270, lw=1))
        ax.add_patch(Arc((x, y-r/2), r, r, angle=0, theta1=0, theta2=180, lw=1))
        ax.add_patch(Arc((x, y+r/2), r, r, angle=0, theta1=180, theta2=360, lw=1))


def generate_kolam(n=9):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal')
    ax.axis('off')

    # draw dot grid
    for i in range(n):
        for j in range(n):
            ax.add_patch(Circle((i, j), 0.05, color='black'))

    rules = {}
    for i in range((n+1)//2):
        for j in range((n+1)//2):
            rule = random.randint(0,5)
            for (dx, dy) in [(i,j), (n-1-i,j), (i,n-1-j), (n-1-i,n-1-j)]:
                rules[(dx,dy)] = rule

    # draw curves
    for (x,y), rule in rules.items():
        draw_curve(ax, x, y, rule)

    plt.show()

# Run it
generate_kolam(9)

