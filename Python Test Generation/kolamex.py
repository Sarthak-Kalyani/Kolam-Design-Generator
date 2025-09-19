import turtle
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

# ---------------- Turtle screen ----------------
screen = turtle.Screen()
screen.title("Traditional Kolam Generator")
screen.bgcolor("white")
pen = turtle.Turtle(visible=False)
pen.speed(0)
pen.pensize(2)

# ---------------- Utilities ----------------
def reset_canvas(rows, cols, spacing):
    pen.clear()
    w = (cols - 1) * spacing + 260
    h = (rows - 1) * spacing + 260
    screen.setup(width=int(w), height=int(h))

def grid_offsets(rows, cols, spacing):
    ox = -((cols - 1) * spacing) / 2
    oy =  ((rows - 1) * spacing) / 2
    return ox, oy

def draw_dot_grid(rows, cols, spacing, ox, oy):
    pen.color("black"); pen.pensize(1)
    for r in range(rows):
        for c in range(cols):
            pen.penup()
            pen.goto(ox + c*spacing, oy - r*spacing)
            pen.dot(6, "black")
    pen.pensize(2)

# quarter-arc helper from a cell center
def arc_from_cell_center(cx, cy, r, heading, extent=90):
    pen.penup(); pen.goto(cx, cy); pen.setheading(heading)
    pen.forward(r); pen.right(90)
    pen.pendown(); pen.circle(r, extent)

# ---------------- Kolam patterns (traditional) ----------------
def pattern_sikku_all(rows, cols, spacing, ox, oy, color="#222"):
    """
    Sikku (kambi) loops around EVERY 2x2 cell: symmetric rounded squares.
    Looks like classic pulli kolam loops covering the grid.
    """
    pen.color(color)
    r = spacing/2
    for i in range(rows-1):
        for j in range(cols-1):
            cx = ox + j*spacing + spacing/2
            cy = oy - i*spacing - spacing/2
            # four rounded corners make one loop
            arc_from_cell_center(cx, cy, r, 0)
            arc_from_cell_center(cx, cy, r, 90)
            arc_from_cell_center(cx, cy, r, 180)
            arc_from_cell_center(cx, cy, r, 270)

def pattern_sikku_interleave(rows, cols, spacing, ox, oy, color="#111"):
    """
    Interleaved sikku: draw on a checkerboard so lobes weave visually.
    """
    pen.color(color)
    r = spacing/2
    for i in range(rows-1):
        for j in range(cols-1):
            if (i + j) % 2 == 0:
                cx = ox + j*spacing + spacing/2
                cy = oy - i*spacing - spacing/2
                pen.penup(); pen.goto(cx, cy - r); pen.setheading(0)
                pen.pendown()
                for _ in range(4):
                    pen.circle(r, 180)
                    pen.left(90)

def pattern_diamond_net(rows, cols, spacing, ox, oy, color="#600"):
    """
    Diamond mesh formed by joining midpoints of each 2x2 cell.
    Very traditional lattice that looks like kolam 'net'.
    """
    pen.color(color)
    for i in range(rows-1):
        for j in range(cols-1):
            x1 = ox + j*spacing
            y1 = oy - i*spacing
            x2 = x1 + spacing
            y2 = y1 - spacing
            m_top    = ((x1+x2)/2, y1)
            m_right  = (x2, (y1+y2)/2)
            m_bottom = ((x1+x2)/2, y2)
            m_left   = (x1, (y1+y2)/2)
            # draw the diamond
            pen.penup(); pen.goto(*m_top); pen.pendown()
            pen.goto(*m_right); pen.goto(*m_bottom)
            pen.goto(*m_left);  pen.goto(*m_top)

def pattern_neli_snake(rows, cols, spacing, ox, oy, color="#064"):
    """
    Neli (snake) kolam: single serpentine path weaving between columns,
    alternating semicircles so it flows around dots. Continuous per row.
    """
    pen.color(color)
    r = spacing/2
    pen.penup()
    # start just left of first dot row
    y0 = oy
    x_start = ox - r
    for i in range(rows):
        y = y0 - i*spacing
        pen.goto(x_start, y)
        pen.setheading(0)
        pen.pendown()
        # draw across columns with alternating bulge
        direction_up = (i % 2 == 0)
        for j in range(cols-1):
            if direction_up:
                pen.circle(r, 180)  # bulge up
            else:
                pen.circle(-r, 180) # bulge down
            direction_up = not direction_up
        # connection to next row (U-turn arc) except last row
        if i < rows-1:
            if cols % 2 == 1:  # end on opposite bulge than start, adjust turn
                pen.right(90); pen.penup(); pen.forward(spacing/2); pen.right(90)
                pen.pendown(); pen.circle(r, 180)
            else:
                pen.left(90); pen.penup(); pen.forward(spacing/2); pen.left(90)
                pen.pendown(); pen.circle(-r, 180)
            pen.penup(); pen.goto(pen.xcor(), y - spacing); pen.pendown()

def pattern_lotus_center(rows, cols, spacing, ox, oy, color="#103a8a"):
    """
    Central lotus-like kolam: petals formed by arcs tracing around
    the inner ring of dots (works best on odd grids like 5x5, 7x7).
    """
    pen.color(color)
    if rows < 3 or cols < 3:
        return
    r = spacing/2.2
    # center ring indices
    i_mid = (rows-1)/2
    j_mid = (cols-1)/2
    # four petals around center
    centers = []
    # up
    centers.append((ox + j_mid*spacing, oy - (i_mid-1)*spacing))
    # right
    centers.append((ox + (j_mid+1)*spacing, oy - i_mid*spacing))
    # down
    centers.append((ox + j_mid*spacing, oy - (i_mid+1)*spacing))
    # left
    centers.append((ox + (j_mid-1)*spacing, oy - i_mid*spacing))
    for (cx, cy) in centers:
        pen.penup(); pen.goto(cx, cy - r); pen.setheading(0)
        pen.pendown()
        pen.circle(r, 270)  # fat petal arc
    # small inner circle
    pen.penup()
    pen.goto(ox + j_mid*spacing, oy - i_mid*spacing - r/2)
    pen.setheading(0)
    pen.pendown()
    pen.circle(r/2, 360)

def pattern_combo(rows, cols, spacing, ox, oy):
    """
    Combination kept traditional: overlay sikku_interleave + diamond mesh.
    """
    pattern_sikku_interleave(rows, cols, spacing, ox, oy, color="#000")
    pattern_diamond_net(rows, cols, spacing, ox, oy, color="#b00")

# ---------------- Controller ----------------
PATTERNS = {
    "Sikku (All Cells)":         pattern_sikku_all,
    "Sikku (Interleave)":        pattern_sikku_interleave,
    "Diamond Net":               pattern_diamond_net,
    "Neli Snake (Serpentine)":   pattern_neli_snake,
    "Lotus (Center Petals)":     pattern_lotus_center,
    "Combination (Sikku+Net)":   pattern_combo,
}

def draw_pattern(name, rows, cols, spacing):
    screen.tracer(False)   # FAST
    reset_canvas(rows, cols, spacing)
    ox, oy = grid_offsets(rows, cols, spacing)
    draw_dot_grid(rows, cols, spacing, ox, oy)
    func = PATTERNS.get(name, pattern_sikku_all)
    func(rows, cols, spacing, ox, oy) if name != "Combination (Sikku+Net)" else func(rows, cols, spacing, ox, oy)
    screen.update()
    # reset turtle state
    pen.penup(); pen.home(); pen.setheading(0); pen.hideturtle()

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

# ---------------- Tkinter GUI ----------------
root = tk.Tk()
root.title("Kolam Generator (Traditional)")
root.geometry("420x310")

tk.Label(root, text="Rows:").grid(row=0, column=0, pady=6, sticky="e")
rows_entry = tk.Entry(root); rows_entry.insert(0, "5"); rows_entry.grid(row=0, column=1)

tk.Label(root, text="Cols:").grid(row=1, column=0, pady=6, sticky="e")
cols_entry = tk.Entry(root); cols_entry.insert(0, "5"); cols_entry.grid(row=1, column=1)

tk.Label(root, text="Spacing:").grid(row=2, column=0, pady=6, sticky="e")
spacing_entry = tk.Entry(root); spacing_entry.insert(0, "60"); spacing_entry.grid(row=2, column=1)

tk.Label(root, text="Kolam Type:").grid(row=3, column=0, pady=6, sticky="e")
pattern_menu = ttk.Combobox(
    root, values=list(PATTERNS.keys()), state="readonly", width=28
)
pattern_menu.grid(row=3, column=1)
pattern_menu.set("Sikku (All Cells)")   # default

def run_drawing():
    try:
        rows = max(3, int(rows_entry.get()))
        cols = max(3, int(cols_entry.get()))
        spacing = max(30, int(spacing_entry.get()))
    except Exception:
        messagebox.showerror("Input error", "Rows/Cols/Spacing must be integers.")
        return
    draw_pattern(pattern_menu.get(), rows, cols, spacing)  # <-- IMPORTANT

tk.Button(root, text="Draw Kolam", command=run_drawing, bg="#cfe8ff").grid(row=4, column=0, columnspan=2, pady=12)
tk.Button(root, text="Save Kolam", command=save_as_image, bg="#c8f7c5").grid(row=5, column=0, columnspan=2, pady=4)

root.mainloop()
