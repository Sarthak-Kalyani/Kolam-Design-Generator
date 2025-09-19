# kolam_master.py
import turtle
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

# ---------------- Turtle / Screen setup ----------------
screen = turtle.Screen()
screen.title("Kolam Master — Traditional Kolams")
screen.bgcolor("black")

pen = turtle.Turtle(visible=False)
pen.speed(0)
pen.pensize(2)
pen.color("white")

# Use manual tracer control for fast drawing
def begin_fast():
    try:
        screen.tracer(False)
    except Exception:
        pass

def end_fast():
    try:
        screen.update()
        screen.tracer(True)
    except Exception:
        pass

# ---------------- Utilities ----------------
def reset_canvas(rows, cols, spacing):
    pen.clear()
    w = int((cols - 1) * spacing + 260)
    h = int((rows - 1) * spacing + 260)
    screen.setup(width=w, height=h)

def grid_offsets(rows, cols, spacing):
    # center the grid
    ox = -((cols - 1) * spacing) / 2
    oy = ((rows - 1) * spacing) / 2
    return ox, oy

def draw_dot_grid(rows, cols, spacing, ox, oy):
    pen.pensize(1)
    pen.color("white")
    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing
            y = oy - r * spacing
            pen.penup(); pen.goto(x, y)
            pen.dot(6, "white")
    pen.pensize(2)

def reset_cursor():
    pen.penup(); pen.home(); pen.setheading(0); pen.hideturtle()

# helper arc from center (for sikku style)
def arc_from_center(cx, cy, r, heading, extent=90):
    pen.penup(); pen.goto(cx, cy); pen.setheading(heading)
    pen.forward(r); pen.right(90)
    pen.pendown(); pen.circle(r, extent)

# ---------------- Real Kolam patterns (dot-grid based) ----------------

def pattern_simple_diamond(rows, cols, spacing, ox, oy, color="white"):
    """Classic diamond around each dot (you liked this)."""
    pen.color(color)
    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing
            y = oy - r * spacing
            # diamond centered on each dot (small)
            half = spacing / 2.2
            pen.penup(); pen.goto(x - half, y)
            pen.pendown()
            pen.goto(x, y + half)
            pen.goto(x + half, y)
            pen.goto(x, y - half)
            pen.goto(x - half, y)

def pattern_diamond_star(rows, cols, spacing, ox, oy, color="cyan"):
    """Diamond plus diagonal star connections (diamond-star hybrid)."""
    pen.color(color)
    half = spacing / 2.2
    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing
            y = oy - r * spacing
            # diamond
            pen.penup(); pen.goto(x - half, y); pen.pendown()
            pen.goto(x, y + half); pen.goto(x + half, y); pen.goto(x, y - half); pen.goto(x - half, y)
            # diagonals (short cross lines) to form star segments
            d = half * 0.7
            pen.penup(); pen.goto(x - d, y - d); pen.pendown(); pen.goto(x + d, y + d)
            pen.penup(); pen.goto(x - d, y + d); pen.pendown(); pen.goto(x + d, y - d)

def pattern_multi_layer_diamond(rows, cols, spacing, ox, oy, color="gold"):
    """Multiple concentric diamond loops around each dot for a layered effect."""
    pen.color(color)
    for r0 in range(rows):
        for c0 in range(cols):
            x = ox + c0 * spacing
            y = oy - r0 * spacing
            # three layers
            for scale in (0.5, 0.33, 0.18):
                half = spacing * scale
                pen.penup(); pen.goto(x - half, y); pen.pendown()
                pen.goto(x, y + half); pen.goto(x + half, y); pen.goto(x, y - half); pen.goto(x - half, y)

def pattern_maze_diamond(rows, cols, spacing, ox, oy, color="lightgreen"):
    """Maze-like smooth loops using semicircles around each 2x2 cell."""
    pen.color(color)
    r = spacing / 2.0
    for rcell in range(rows - 1):
        for ccell in range(cols - 1):
            cx = ox + ccell * spacing + spacing/2
            cy = oy - rcell * spacing - spacing/2
            # draw rounded diamond loop: sequence of arcs
            pen.penup(); pen.goto(cx - r, cy); pen.setheading(0); pen.pendown()
            for _ in range(4):
                pen.circle(r, 180)
                pen.right(90)

def pattern_lotus_center(rows, cols, spacing, ox, oy, color="magenta"):
    """Centered lotus style using mid-ring of dots (best if grid odd)."""
    pen.color(color)
    if rows < 3 or cols < 3:
        return
    mid_r = (rows - 1) // 2
    mid_c = (cols - 1) // 2
    cx = ox + mid_c * spacing
    cy = oy - mid_r * spacing
    r = spacing * 0.9
    petals = 8
    pen.penup(); pen.goto(cx, cy - r/2); pen.pendown()
    for i in range(petals):
        pen.circle(r/2, 120)
        pen.left(180 - 120)
        pen.circle(r/2, 120)
        pen.left(180 - 360 / petals)

    # small center ring
    pen.penup(); pen.goto(cx, cy - r/6); pen.pendown(); pen.circle(r/6)

def pattern_petal_grid(rows, cols, spacing, ox, oy, color="orange"):
    """Petal arcs around every dot (grid of petals)."""
    pen.color(color)
    rp = spacing / 2.5
    for r0 in range(rows):
        for c0 in range(cols):
            x = ox + c0 * spacing
            y = oy - r0 * spacing
            for angle in (0, 90, 180, 270):
                pen.penup(); pen.goto(x, y); pen.setheading(angle); pen.forward(rp)
                pen.pendown(); pen.circle(rp, 180)

def pattern_infinity_cells(rows, cols, spacing, ox, oy, color="purple"):
    """Infinity loops around each 2x2 cell (continuous figure-8 feel)."""
    pen.color(color)
    r = spacing / 2.3
    for rcell in range(rows - 1):
        for ccell in range(cols - 1):
            cx = ox + ccell * spacing + spacing/2
            cy = oy - rcell * spacing - spacing/2
            pen.penup(); pen.goto(cx - r, cy); pen.setheading(0); pen.pendown()
            # figure-8: two circles joined
            pen.circle(r, 180)
            pen.circle(-r, 180)

def pattern_concentric_loops(rows, cols, spacing, ox, oy, color="lightblue"):
    """Concentric loops around center of grid (big rings)."""
    pen.color(color)
    midx = ox + (cols - 1) * spacing / 2
    midy = oy - (rows - 1) * spacing / 2
    maxr = min(cols, rows) * spacing / 1.75
    steps = int(min(cols, rows) / 1.0) + 1
    for i in range(1, steps):
        r = maxr * (i / steps)
        pen.penup(); pen.goto(midx, midy - r); pen.pendown()
        pen.circle(r)

def pattern_neli_snake(rows, cols, spacing, ox, oy, color="green"):
    """Serpentine continuous snake weaving across rows (Neli kolam feel)."""
    pen.color(color)
    r = spacing / 2.2
    start_x = ox - spacing/2
    for i in range(rows):
        y = oy - i * spacing
        pen.penup(); pen.goto(start_x, y); pen.setheading(0); pen.pendown()
        # across the row
        for j in range(cols - 1):
            if i % 2 == 0:
                pen.circle(r, 180)
            else:
                pen.circle(-r, 180)
            pen.forward(spacing / 10)
        # step down connection
        if i < rows - 1:
            pen.penup(); pen.goto(pen.xcor(), y - spacing/2); pen.pendown()
            pen.circle(r if i % 2 == 0 else -r, 180)

# ---------------- Patterns dictionary (keep older good ones + new) ----------------
PATTERNS = {
    "Simple Diamond":            pattern_simple_diamond,
    "Diamond + Star":            pattern_diamond_star,
    "Multi-Layer Diamond":       pattern_multi_layer_diamond,
    "Maze Diamond":              pattern_maze_diamond,
    "Lotus (center)":            pattern_lotus_center,
    "Petal Grid":                pattern_petal_grid,
    "Infinity Cells":            pattern_infinity_cells,
    "Concentric Loops":          pattern_concentric_loops,
    "Neli Snake (serpentine)":   pattern_neli_snake,
}

# ---------------- Controller ----------------
def draw_pattern(name, rows, cols, spacing):
    begin_fast()
    reset_canvas(rows, cols, spacing)
    ox, oy = grid_offsets(rows, cols, spacing)
    draw_dot_grid(rows, cols, spacing, ox, oy)
    func = PATTERNS.get(name, pattern_simple_diamond)
    # call pattern
    func(rows, cols, spacing, ox, oy)
    end_fast()
    reset_cursor()

# ---------------- Save image ----------------
def save_as_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg")])
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

# ---------------- Tkinter GUI ----------------
root = tk.Tk()
root.title("Kolam Master (Traditional)")
root.geometry("480x360")

# Inputs
tk.Label(root, text="Rows (dots):").grid(row=0, column=0, sticky="e", pady=6, padx=6)
rows_entry = tk.Entry(root); rows_entry.insert(0, "7"); rows_entry.grid(row=0, column=1)

tk.Label(root, text="Cols (dots):").grid(row=1, column=0, sticky="e", pady=6, padx=6)
cols_entry = tk.Entry(root); cols_entry.insert(0, "7"); cols_entry.grid(row=1, column=1)

tk.Label(root, text="Spacing (px):").grid(row=2, column=0, sticky="e", pady=6, padx=6)
spacing_entry = tk.Entry(root); spacing_entry.insert(0, "48"); spacing_entry.grid(row=2, column=1)

tk.Label(root, text="Kolam Type:").grid(row=3, column=0, sticky="e", pady=6, padx=6)
pattern_menu = ttk.Combobox(root, values=list(PATTERNS.keys()), state="readonly", width=30)
pattern_menu.grid(row=3, column=1)
pattern_menu.set("Simple Diamond")

def run_drawing():
    try:
        rows = max(3, int(rows_entry.get()))
        cols = max(3, int(cols_entry.get()))
        spacing = max(20, int(spacing_entry.get()))
    except Exception:
        messagebox.showerror("Input error", "Rows/Cols/Spacing must be integers.")
        return
    draw_pattern(pattern_menu.get(), rows, cols, spacing)

tk.Button(root, text="Draw Kolam", command=run_drawing, bg="#cfe8ff").grid(row=4, column=0, columnspan=2, pady=12)
tk.Button(root, text="Save Kolam", command=save_as_image, bg="#c8f7c5").grid(row=5, column=0, columnspan=2, pady=4)

# Helpful quick presets row
def preset_odd7():
    rows_entry.delete(0, tk.END); rows_entry.insert(0, "7")
    cols_entry.delete(0, tk.END); cols_entry.insert(0, "7")
    spacing_entry.delete(0, tk.END); spacing_entry.insert(0, "48")
def preset_5x5():
    rows_entry.delete(0, tk.END); rows_entry.insert(0, "5")
    cols_entry.delete(0, tk.END); cols_entry.insert(0, "5")
    spacing_entry.delete(0, tk.END); spacing_entry.insert(0, "60")

tk.Button(root, text="Preset 7×7", command=preset_odd7).grid(row=6, column=0, pady=6)
tk.Button(root, text="Preset 5×5", command=preset_5x5).grid(row=6, column=1, pady=6)

root.mainloop()
