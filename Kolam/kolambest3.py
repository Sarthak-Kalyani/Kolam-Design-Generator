# kolam_master_fixed.py
import turtle
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

# ---------------- Turtle / Screen setup ----------------
screen = turtle.Screen()
screen.title("Kolam Master — Traditional Kolams")
screen.bgcolor("white")

pen = turtle.Turtle(visible=False)
pen.speed(0)
pen.pensize(2)
pen.color("black")

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

# ---------------- Real Kolam patterns ----------------
def pattern_simple_diamond(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing
            y = oy - r * spacing
            half = spacing / 2.2
            pen.penup(); pen.goto(x - half, y)
            pen.pendown()
            pen.goto(x, y + half)
            pen.goto(x + half, y)
            pen.goto(x, y - half)
            pen.goto(x - half, y)

def pattern_diamond_star(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    half = spacing / 2.2
    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing
            y = oy - r * spacing
            # diamond
            pen.penup(); pen.goto(x - half, y); pen.pendown()
            pen.goto(x, y + half); pen.goto(x + half, y); pen.goto(x, y - half); pen.goto(x - half, y)
            # diagonals
            d = half * 0.7
            pen.penup(); pen.goto(x - d, y - d); pen.pendown(); pen.goto(x + d, y + d)
            pen.penup(); pen.goto(x - d, y + d); pen.pendown(); pen.goto(x + d, y - d)

def pattern_multi_layer_diamond(rows, cols, spacing, ox, oy, color="black"):
    pen.color(color)
    for r0 in range(rows):
        for c0 in range(cols):
            x = ox + c0 * spacing
            y = oy - r0 * spacing
            for scale in (0.5, 0.33, 0.18):
                half = spacing * scale
                pen.penup(); pen.goto(x - half, y); pen.pendown()
                pen.goto(x, y + half); pen.goto(x + half, y); pen.goto(x, y - half); pen.goto(x - half, y)

def pattern_maze_diamond(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    r = spacing / 2.0
    for rcell in range(rows - 1):
        for ccell in range(cols - 1):
            cx = ox + ccell * spacing + spacing/2
            cy = oy - rcell * spacing - spacing/2
            pen.penup(); pen.goto(cx - r, cy); pen.setheading(0); pen.pendown()
            for _ in range(4):
                pen.circle(r, 180)
                pen.right(90)

def pattern_petal_grid(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    rp = spacing / 2.5
    for r0 in range(rows):
        for c0 in range(cols):
            x = ox + c0 * spacing
            y = oy - r0 * spacing
            for angle in (0, 90, 180, 270):
                pen.penup(); pen.goto(x, y); pen.setheading(angle); pen.forward(rp)
                pen.pendown(); pen.circle(rp, 180)

def pattern_infinity_cells(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    size = spacing / 1.5
    for i in range(18):
        pen.circle(size, 90)
        pen.circle(-size, 90)
        pen.right(20)

def pattern_concentric_loops(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    midx = ox + (cols - 1) * spacing / 2
    midy = oy - (rows - 1) * spacing / 2
    maxr = min(cols, rows) * spacing / 1.75
    steps = int(min(cols, rows) / 1.0) + 1
    for i in range(1, steps):
        r = maxr * (i / steps)
        pen.penup(); pen.goto(midx, midy - r); pen.pendown()
        pen.circle(r)

# -------- Replaced patterns (from your working code) --------
def pattern_square(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    size = spacing
    for i in range(36):
        pen.penup(); pen.goto(0, 0); pen.pendown()
        pen.forward(size)
        pen.right(100)

def pattern_lotus_center(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    pen.penup(); pen.goto(0, -100); pen.pendown()
    for i in range(36):
        pen.circle(100, steps=6)
        pen.right(170)

def pattern_neli_snake(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    size = 20
    for i in range(60):
        pen.circle(size, 180)
        pen.circle(-size, 180)

def pattern_spiral(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    for i in range(80):
        pen.circle(i*2, 90)

def pattern_star(rows, cols, spacing, ox, oy, color="white"):
    pen.color(color)
    size = 150
    for i in range(36):
        pen.forward(size)
        pen.right(170)

# ---------------- Patterns dictionary ----------------
PATTERNS = {
    "Simple Diamond":        pattern_simple_diamond,
    "Diamond + Star":        pattern_diamond_star,
    "Multi-Layer Diamond":   pattern_multi_layer_diamond,
    "Maze Diamond":          pattern_maze_diamond,
    "Petal Grid":            pattern_petal_grid,
    "Infinity Cells":        pattern_infinity_cells,
    "Concentric Loops":      pattern_concentric_loops,
    "Square Kolam":          pattern_square,
    "Lotus (Centre)":        pattern_lotus_center,
    "Neli Snake":            pattern_neli_snake,
    "Spiral Kolam":          pattern_spiral,
    "Star Kolam":            pattern_star,
}

# ---------------- Controller ----------------
def draw_pattern(name, rows, cols, spacing):
    begin_fast()
    reset_canvas(rows, cols, spacing)
    ox, oy = grid_offsets(rows, cols, spacing)
    draw_dot_grid(rows, cols, spacing, ox, oy)
    func = PATTERNS.get(name, pattern_simple_diamond)
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
root.geometry("480x380")

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
