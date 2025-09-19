# kolam_generator.py
# Python 3.x
# Requirements:
#  - builtin: turtle, tkinter, time, math, os
#  - optional: Pillow (PIL) for saving to PNG (pip install pillow)

import turtle
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import math
import os

# Optional PIL import for converting postscript -> png
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ----- Configurable parameters -----
WINDOW_W, WINDOW_H = 900, 700
GRID_ROWS = 7
GRID_COLS = 7
DOT_SPACING = 40  # pixels between dots
DOT_RADIUS = 3

# ----- Helper: turtle & tkinter setup -----
root = tk.Tk()
root.title("Kolam Generator — Turtle")
root.geometry(f"{WINDOW_W}x{WINDOW_H}")

canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create turtle canvas inside the tkinter frame
cv = tk.Canvas(canvas_frame, width=WINDOW_W*0.66, height=WINDOW_H, bg="white")
cv.pack(fill=tk.BOTH, expand=True)

screen = turtle.TurtleScreen(cv)
screen.bgcolor("white")

# Speed control - we'll use tracer to speed up drawing
draw_turtle = turtle.RawTurtle(screen)
dot_turtle = turtle.RawTurtle(screen)
draw_turtle.hideturtle()
dot_turtle.hideturtle()
draw_turtle.speed(0)
dot_turtle.speed(0)

# Use tracer for large drawings (0 = no automatic updates)
screen.tracer(0, 0)

# Track last drawn positions to enable clear/redo
CURRENT_PATTERN = None
LAST_GRID = None

# Calculate grid coordinates (centered)
def compute_grid(rows=GRID_ROWS, cols=GRID_COLS, spacing=DOT_SPACING):
    total_w = (cols - 1) * spacing
    total_h = (rows - 1) * spacing
    start_x = -total_w / 2
    start_y = total_h / 2
    coords = []
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * spacing
            y = start_y - r * spacing
            coords.append((x, y))
    return coords

# Draw dot grid
def draw_dot_grid(rows=GRID_ROWS, cols=GRID_COLS, spacing=DOT_SPACING, dot_radius=DOT_RADIUS):
    global LAST_GRID
    LAST_GRID = compute_grid(rows, cols, spacing)
    dot_turtle.clear()
    dot_turtle.penup()
    for (x, y) in LAST_GRID:
        dot_turtle.goto(x, y - dot_radius)  # slight offset so circle is centered
        dot_turtle.dot(dot_radius * 2)
    screen.update()

# Utility: move turtle safely without drawing
def move_to(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

# Pattern functions: Accept grid (list of coords) and draw
def pattern_diamond(grid):
    # Diamond kolam: connect square-like diamonds across grid
    # We'll take central rows and draw diamond paths around dot centers
    if not grid:
        return
    # Convert grid to 2D matrix for indexing
    rows = GRID_ROWS; cols = GRID_COLS
    mat = [grid[i*cols:(i+1)*cols] for i in range(rows)]
    draw_turtle.clear()
    draw_turtle.width(2)
    for r in range(rows - 1):
        for c in range(cols - 1):
            # each cell: 4 corners, draw a diamond ring around cell center
            p1 = mat[r][c]
            p2 = mat[r][c+1]
            p3 = mat[r+1][c+1]
            p4 = mat[r+1][c]
            cx = (p1[0]+p2[0]+p3[0]+p4[0])/4
            cy = (p1[1]+p2[1]+p3[1]+p4[1])/4
            # diamond around (cx,cy)
            pts = [(cx, cy + DOT_SPACING/2),
                   (cx + DOT_SPACING/2, cy),
                   (cx, cy - DOT_SPACING/2),
                   (cx - DOT_SPACING/2, cy)]
            move_to(draw_turtle, *pts[-1])
            draw_turtle.begin_fill()
            draw_turtle.fillcolor("")  # no fill
            for px, py in pts:
                draw_turtle.goto(px, py)
            draw_turtle.goto(pts[0][0], pts[0][1])
            draw_turtle.end_fill()
    screen.update()

def pattern_star(grid):
    # Star-like loops connecting rings around selected central points
    if not grid:
        return
    draw_turtle.clear()
    draw_turtle.width(2)
    rows = GRID_ROWS; cols = GRID_COLS
    mat = [grid[i*cols:(i+1)*cols] for i in range(rows)]
    center_r = rows // 2
    center_c = cols // 2
    # draw radial star from center dot
    cx, cy = mat[center_r][center_c]
    move_to(draw_turtle, cx, cy)
    big_r = DOT_SPACING * min(rows, cols) * 0.35
    spikes = 8
    for i in range(spikes):
        ang = 2*math.pi*i/spikes
        x = cx + math.cos(ang)*big_r
        y = cy + math.sin(ang)*big_r
        draw_turtle.goto(x, y)
        draw_turtle.goto(cx, cy)
    # outer loop: rounded star outline using simple arcs
    for i in range(spikes):
        ang1 = 2*math.pi*i/spikes
        ang2 = 2*math.pi*(i+1)/spikes
        x1 = cx + math.cos(ang1)*big_r
        y1 = cy + math.sin(ang1)*big_r
        x2 = cx + math.cos(ang2)*big_r
        y2 = cy + math.sin(ang2)*big_r
        move_to(draw_turtle, x1, y1)
        draw_turtle.goto((x1+x2)/2, (y1+y2)/2 - DOT_SPACING*0.2)
        draw_turtle.goto(x2, y2)
    screen.update()

def pattern_lotus(grid):
    # Lotus petals around center using bezier-like curves approximated by arcs
    if not grid:
        return
    draw_turtle.clear()
    draw_turtle.width(2)
    rows = GRID_ROWS; cols = GRID_COLS
    mat = [grid[i*cols:(i+1)*cols] for i in range(rows)]
    cx, cy = mat[rows//2][cols//2]
    petals = 6
    r_outer = DOT_SPACING * 1.7
    for i in range(petals):
        ang = 2*math.pi*i/petals
        # petal tip
        tx = cx + math.cos(ang)*r_outer
        ty = cy + math.sin(ang)*r_outer
        # control points for a smooth petal
        move_to(draw_turtle, cx, cy)
        draw_turtle.goto(tx, ty)
        # make a curved return using a short arc approximation
        mid_ang = ang + math.pi/petals
        mx = cx + math.cos(mid_ang)*r_outer*0.6
        my = cy + math.sin(mid_ang)*r_outer*0.6
        draw_turtle.goto(mx, my)
        draw_turtle.goto(cx, cy)
    screen.update()

def pattern_butterfly(grid):
    # Butterfly/infinity loops across center rows
    if not grid:
        return
    draw_turtle.clear()
    draw_turtle.width(2)
    rows = GRID_ROWS; cols = GRID_COLS
    mat = [grid[i*cols:(i+1)*cols] for i in range(rows)]
    cx, cy = mat[rows//2][cols//2]
    # two loops left & right
    r = DOT_SPACING * 1.3
    # left loop
    move_to(draw_turtle, cx - r, cy)
    for t in range(0, 181, 4):
        a = math.radians(t)
        x = cx - r + math.cos(a)*r
        y = cy + math.sin(a)*r*0.6
        draw_turtle.goto(x, y)
    # right loop
    move_to(draw_turtle, cx + r, cy)
    for t in range(0, 181, 4):
        a = math.radians(t)
        x = cx + r - math.cos(a)*r
        y = cy + math.sin(a)*r*0.6
        draw_turtle.goto(x, y)
    # connecting figure-8 center lines
    move_to(draw_turtle, cx - r*0.6, cy)
    draw_turtle.goto(cx + r*0.6, cy)
    screen.update()

def pattern_spiral(grid):
    # Circular spiral kolam radiating from center
    if not grid:
        return
    draw_turtle.clear()
    draw_turtle.width(2)
    rows = GRID_ROWS; cols = GRID_COLS
    mat = [grid[i*cols:(i+1)*cols] for i in range(rows)]
    cx, cy = mat[rows//2][cols//2]
    move_to(draw_turtle, cx, cy)
    steps = 300
    a = 0.0
    max_r = DOT_SPACING * min(rows, cols) * 0.5
    for i in range(steps):
        r = (i/steps) * max_r
        a += 0.25
        x = cx + math.cos(a) * r
        y = cy + math.sin(a) * r
        draw_turtle.goto(x, y)
    screen.update()

# Master draw handler
def draw_pattern(name):
    global CURRENT_PATTERN
    if not LAST_GRID:
        draw_dot_grid()
    CURRENT_PATTERN = name
    if name == "Diamond":
        pattern_diamond(LAST_GRID)
    elif name == "Star":
        pattern_star(LAST_GRID)
    elif name == "Lotus":
        pattern_lotus(LAST_GRID)
    elif name == "Butterfly":
        pattern_butterfly(LAST_GRID)
    elif name == "Spiral":
        pattern_spiral(LAST_GRID)

# Clear drawings (keeps dots)
def clear_drawing():
    global CURRENT_PATTERN
    draw_turtle.clear()
    CURRENT_PATTERN = None
    screen.update()

# Full reset: clear everything and redraw dots
def reset_all():
    draw_turtle.clear()
    dot_turtle.clear()
    screen.update()
    draw_dot_grid()

# Save function: save postscript then convert with PIL if available
def save_image():
    # ask filename
    fname = filedialog.asksaveasfilename(defaultextension=".png",
                                         filetypes=[("PNG image", "*.png"), ("PostScript", "*.ps")],
                                         title="Save kolam image as")
    if not fname:
        return
    base, ext = os.path.splitext(fname)
    ps_path = base + ".ps"
    # Get tkinter canvas and generate postscript
    try:
        cv.postscript(file=ps_path, colormode='color')
    except Exception as e:
        messagebox.showerror("Save error", f"Could not save postscript: {e}")
        return
    if ext.lower() == ".ps":
        messagebox.showinfo("Saved", f"Saved PostScript to {ps_path}")
        return
    # if user asked for png and PIL available, convert
    if PIL_AVAILABLE:
        try:
            img = Image.open(ps_path)
            # Trim whitespace: optional
            bbox = img.getbbox()
            if bbox:
                img = img.crop(bbox)
            img.save(fname, "PNG")
            messagebox.showinfo("Saved", f"Saved PNG to {fname}")
            # remove ps file if you like:
            try:
                os.remove(ps_path)
            except OSError:
                pass
        except Exception as e:
            messagebox.showerror("Conversion error", f"Could not convert to PNG: {e}\nPS saved at {ps_path}")
    else:
        messagebox.showinfo("Saved PS", f"Pillow not available. Saved PostScript at {ps_path}. To get PNG/PNG use `pip install pillow` and convert the .ps file.")

# UI controls (right side)
control_frame = tk.Frame(root, width=260)
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(control_frame, text="Kolam Generator", font=("Arial", 14, "bold")).pack(pady=8)

# Pattern buttons
patterns = ["Diamond", "Star", "Lotus", "Butterfly", "Spiral"]
pattern_var = tk.StringVar(value=patterns[0])

for p in patterns:
    b = ttk.Radiobutton(control_frame, text=p, value=p, variable=pattern_var)
    b.pack(anchor="w", padx=10, pady=2)

def on_draw():
    name = pattern_var.get()
    draw_pattern(name)

draw_btn = ttk.Button(control_frame, text="Draw Pattern", command=on_draw)
draw_btn.pack(pady=8, fill=tk.X, padx=10)

clear_btn = ttk.Button(control_frame, text="Clear (Keep Dots)", command=clear_drawing)
clear_btn.pack(pady=4, fill=tk.X, padx=10)

reset_btn = ttk.Button(control_frame, text="Reset Grid", command=reset_all)
reset_btn.pack(pady=4, fill=tk.X, padx=10)

save_btn = ttk.Button(control_frame, text="Save as PNG/PS", command=save_image)
save_btn.pack(pady=10, fill=tk.X, padx=10)

# Controls for grid settings
tk.Label(control_frame, text="Grid rows/cols").pack(pady=(12,0))
rows_spin = tk.Spinbox(control_frame, from_=3, to=15, width=6)
rows_spin.delete(0, "end"); rows_spin.insert(0, str(GRID_ROWS))
rows_spin.pack(padx=10, pady=2)

cols_spin = tk.Spinbox(control_frame, from_=3, to=15, width=6)
cols_spin.delete(0, "end"); cols_spin.insert(0, str(GRID_COLS))
cols_spin.pack(padx=10, pady=2)

tk.Label(control_frame, text="Spacing").pack(pady=(8,0))
spacing_spin = tk.Spinbox(control_frame, from_=20, to=100, width=6)
spacing_spin.delete(0, "end"); spacing_spin.insert(0, str(DOT_SPACING))
spacing_spin.pack(padx=10, pady=2)

def apply_grid_settings():
    global GRID_ROWS, GRID_COLS, DOT_SPACING
    try:
        GRID_ROWS = int(rows_spin.get())
        GRID_COLS = int(cols_spin.get())
        DOT_SPACING = int(spacing_spin.get())
    except Exception:
        messagebox.showerror("Error", "Invalid grid settings")
        return
    draw_dot_grid(GRID_ROWS, GRID_COLS, DOT_SPACING)

apply_btn = ttk.Button(control_frame, text="Apply Grid Settings", command=apply_grid_settings)
apply_btn.pack(pady=6, padx=10, fill=tk.X)

# Speed slider
tk.Label(control_frame, text="(Turtle speed is instant; tracer used)").pack(pady=(12,0))

# Footer note
note = tk.Label(control_frame, text="Tip: Use 'Apply Grid' then 'Draw Pattern'.\nInstall Pillow to save PNGs.", wraplength=220, justify="left")
note.pack(side=tk.BOTTOM, pady=12)

# Initialize grid/dots
draw_dot_grid(GRID_ROWS, GRID_COLS, DOT_SPACING)

# Run tkinter mainloop
def on_closing():
    if messagebox.askokcancel("Quit", "Quit kolam generator?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
