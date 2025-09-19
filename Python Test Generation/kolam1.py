import turtle
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import math
import random

# ---------------- Screen & Turtle ----------------
screen = turtle.Screen()
screen.title("Kolam Generator")
screen.bgcolor("white")

pen = turtle.Turtle(visible=True)
pen.speed(0)
pen.hideturtle()

# ---------------- Helpers ----------------
def reset_canvas(rows, cols, spacing):
    pen.clear()
    total_width = (cols - 1) * spacing + 220
    total_height = (rows - 1) * spacing + 220
    screen.setup(width=int(total_width), height=int(total_height))

def grid_offsets(rows, cols, spacing):
    """return (offset_x, offset_y) so grid is centered"""
    ox = -((cols - 1) * spacing) / 2
    oy = ((rows - 1) * spacing) / 2
    return ox, oy

def draw_dot_grid(rows, cols, spacing, ox, oy):
    for y in range(rows):
        for x in range(cols):
            pen.penup()
            pen.goto(ox + x*spacing, oy - y*spacing)
            pen.dot(6, "black")

def quarter_loop(cx, cy, r, start_heading):
    """draw one rounded corner (quarter circle) from cell-center"""
    pen.penup(); pen.goto(cx, cy); pen.setheading(start_heading)
    pen.forward(r); pen.right(90)
    pen.pendown(); pen.circle(r, 90)

# ---------------- Distinct Pattern Functions ----------------
def pattern_cell_loops(rows, cols, spacing, ox, oy, color="saddlebrown"):
    """Rounded square loop INSIDE each 2x2 cell (inspiration: c top-left)."""
    pen.color(color); pen.pensize(2)
    r = spacing/2
    for y in range(rows-1):
        for x in range(cols-1):
            cx = ox + x*spacing + spacing/2
            cy = oy - y*spacing - spacing/2
            # four quarter arcs making a loop
            for h in [0, 90, 180, 270]:
                quarter_loop(cx, cy, r, h)

def pattern_big_clover(rows, cols, spacing, ox, oy, color="peru"):
    """‘Clover’ loops that pass between adjacent cells (inspiration: c top-2)."""
    pen.color(color); pen.pensize(2)
    r = spacing/2
    # draw only on a checker so curves interleave
    for y in range(rows-1):
        for x in range(cols-1):
            if (x+y) % 2 == 0:
                cx = ox + x*spacing + spacing/2
                cy = oy - y*spacing - spacing/2
                # draw four lobes but rotate the entry each time to avoid looking like cell_loops
                pen.penup(); pen.goto(cx, cy - r); pen.setheading(0)
                pen.pendown()
                for _ in range(4):
                    pen.circle(r, 180); pen.left(90)

def pattern_concentric_dots(rows, cols, spacing, ox, oy, color="darkolivegreen"):
    """Multiple circles centered at each dot (inspiration: b & c third)."""
    pen.color(color); pen.pensize(2)
    radii = [spacing/5, spacing/3, spacing/2.2]
    for y in range(rows):
        for x in range(cols):
            cx = ox + x*spacing
            cy = oy - y*spacing
            for r in radii:
                pen.penup(); pen.goto(cx, cy - r)
                pen.pendown(); pen.circle(r)

def pattern_petals(rows, cols, spacing, ox, oy, color="firebrick"):
    """Petals around EACH dot (looks like flowers; very different from loops)."""
    pen.color(color); pen.pensize(2)
    rp = spacing/3
    for y in range(rows):
        for x in range(cols):
            cx = ox + x*spacing
            cy = oy - y*spacing
            for angle in [0, 90, 180, 270]:
                pen.penup(); pen.goto(cx, cy)
                pen.setheading(angle); pen.forward(rp)
                pen.pendown(); pen.circle(rp, 180)

def pattern_diagonal_cross(rows, cols, spacing, ox, oy, color="slateblue"):
    """Straight diagonals across each 2x2 cell (inspiration: b left)."""
    pen.color(color); pen.pensize(2)
    for y in range(rows-1):
        for x in range(cols-1):
            x1 = ox + x*spacing;     y1 = oy - y*spacing
            x2 = x1 + spacing;       y2 = y1 - spacing
            pen.penup(); pen.goto(x1, y1); pen.pendown(); pen.goto(x2, y2)
            pen.penup(); pen.goto(x2, y1); pen.pendown(); pen.goto(x1, y2)

def pattern_grid_lines(rows, cols, spacing, ox, oy, color="teal"):
    """Clean grid connections (inspiration: c fourth)."""
    pen.color(color); pen.pensize(2)
    # horizontals
    for y in range(rows):
        pen.penup(); pen.goto(ox, oy - y*spacing)
        pen.pendown(); pen.goto(ox + (cols-1)*spacing, oy - y*spacing)
    # verticals
    for x in range(cols):
        pen.penup(); pen.goto(ox + x*spacing, oy)
        pen.pendown(); pen.goto(ox + x*spacing, oy - (rows-1)*spacing)

def pattern_star_cells(rows, cols, spacing, ox, oy, color="darkred"):
    """Star placed in each cell center (inspiration: c bottom rows starry look)."""
    pen.color(color); pen.pensize(2)
    size = spacing*0.42
    for y in range(rows-1):
        for x in range(cols-1):
            cx = ox + x*spacing + spacing/2
            cy = oy - y*spacing - spacing/2
            pen.penup(); pen.goto(cx, cy - size/2); pen.setheading(90)
            pen.pendown()
            for _ in range(5):
                pen.forward(size); pen.right(144)

# --------- A simple single-loop (L-system-ish) pattern -----------
def lsystem_string(axiom, rules, iters):
    s = axiom
    for _ in range(iters):
        s = ''.join(rules.get(ch, ch) for ch in s)
    return s

def pattern_single_loop(rows, cols, spacing, ox, oy, color="black"):
    """
    Single continuous path that weaves across the grid (inspiration: c first).
    This uses a tiny L-system to make a knot-like loop scaled to the grid size.
    """
    pen.color(color); pen.pensize(2)
    # Build command string
    axiom = "FX"
    rules = {
        "X": "X+YF+",  # dragon-curve-like, but we draw with arcs
        "Y": "-FX-Y"
    }
    cmd = lsystem_string(axiom, rules, iters=rows+cols-3)

    # scale step to cell size
    step = spacing * 0.7
    r = step/2

    # start from left-top-ish
    sx = ox - spacing*0.4
    sy = oy + spacing*0.4
    pen.penup(); pen.goto(sx, sy); pen.setheading(0); pen.pendown()

    for ch in cmd:
        if ch == "F":
            # draw smooth segment: two quarter-arcs to look kolam-ish
            pen.circle(r, 90); pen.circle(-r, 90)
        elif ch == "+":
            pen.right(90)
        elif ch == "-":
            pen.left(90)
        else:
            # ignore others
            pass

# ---------------- Controller ----------------
PATTERNS = {
    "Cell Loops (2×2)": pattern_cell_loops,
    "Big Clover (interleave)": pattern_big_clover,
    "Concentric Circles": pattern_concentric_dots,
    "Petals at Dots": pattern_petals,
    "Diagonal Cross": pattern_diagonal_cross,
    "Grid Lines": pattern_grid_lines,   
    "Stars in Cells": pattern_star_cells,
    "Single Loop (L-system)": pattern_single_loop,
}

def draw_pattern(name, rows, cols, spacing):
    reset_canvas(rows, cols, spacing)
    ox, oy = grid_offsets(rows, cols, spacing)
    draw_dot_grid(rows, cols, spacing, ox, oy)
    # draw chosen
    func = PATTERNS.get(name, pattern_cell_loops)
    func(rows, cols, spacing, ox, oy)

# ---------------- Save ----------------
def save_as_image():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg")]
    )
    if not file_path:
        return
    try:
        canvas = screen.getcanvas()
        canvas.postscript(file="temp.eps", colormode="color")
        img = Image.open("temp.eps")
        if file_path.lower().endswith(".jpg"):
            img = img.convert("RGB")
        img.save(file_path, dpi=(300, 300))
        messagebox.showinfo("Saved", f"✅ Kolam saved at {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Saving failed.\n{e}")

# ---------------- Tk GUI ----------------
root = tk.Tk()
root.title("Kolam Generator GUI")
root.geometry("380x320")

tk.Label(root, text="Rows:").grid(row=0, column=0, pady=6, sticky="e")
rows_entry = tk.Entry(root); rows_entry.insert(0, "5"); rows_entry.grid(row=0, column=1)

tk.Label(root, text="Cols:").grid(row=1, column=0, pady=6, sticky="e")
cols_entry = tk.Entry(root); cols_entry.insert(0, "5"); cols_entry.grid(row=1, column=1)

tk.Label(root, text="Spacing:").grid(row=2, column=0, pady=6, sticky="e")
spacing_entry = tk.Entry(root); spacing_entry.insert(0, "60"); spacing_entry.grid(row=2, column=1)

tk.Label(root, text="Pattern:").grid(row=3, column=0, pady=6, sticky="e")
pattern_var = tk.StringVar(value="Cell Loops (2×2)")
pattern_menu = ttk.Combobox(
    root, textvariable=pattern_var,
    values=list(PATTERNS.keys()), state="readonly", width=28
)
pattern_menu.grid(row=3, column=1)

def run_drawing():
    try:
        rows = max(2, int(rows_entry.get()))
        cols = max(2, int(cols_entry.get()))
        spacing = max(20, int(spacing_entry.get()))
    except Exception:
        messagebox.showerror("Input error", "Rows/Cols/Spacing must be integers.")
        return
    draw_pattern(pattern_menu.get(), rows, cols, spacing)

tk.Button(root, text="Draw Kolam", command=run_drawing, bg="#cfe8ff").grid(row=4, column=0, columnspan=2, pady=12)
tk.Button(root, text="Save Kolam", command=save_as_image, bg="#c8f7c5").grid(row=5, column=0, columnspan=2, pady=4)

root.mainloop()
