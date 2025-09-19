import turtle
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

# ---------------- Screen & Turtle ----------------
screen = turtle.Screen()
screen.title("Traditional Kolam Generator")
screen.bgcolor("white")

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

# ---------------- Helpers ----------------
def reset_canvas(rows, cols, spacing):
    pen.clear()
    total_width = (cols - 1) * spacing + 300
    total_height = (rows - 1) * spacing + 300
    screen.setup(width=int(total_width), height=int(total_height))
    pen.penup()
    pen.goto(0, 0)
    pen.pendown()

def grid_offsets(rows, cols, spacing):
    ox = -((cols - 1) * spacing) / 2
    oy = ((rows - 1) * spacing) / 2
    return ox, oy

def draw_dot_grid(rows, cols, spacing, ox, oy):
    for y in range(rows):
        for x in range(cols):
            pen.penup()
            pen.goto(ox + x * spacing, oy - y * spacing)
            pen.dot(6, "black")

# ---------------- Kolam Patterns ----------------
def kolam_loops(rows, cols, spacing, ox, oy, color="black"):
    """Classic loop kolam (like figure-8 around dots)."""
    pen.color(color)
    pen.pensize(2)
    r = spacing / 2
    for y in range(rows - 1):
        for x in range(cols - 1):
            cx = ox + x * spacing + spacing / 2
            cy = oy - y * spacing - spacing / 2
            pen.penup(); pen.goto(cx, cy - r)
            pen.pendown()
            for _ in range(4):
                pen.circle(r, 180)
                pen.left(90)

def kolam_flower(rows, cols, spacing, ox, oy, color="darkblue"):
    """Flower-style petals around each dot."""
    pen.color(color)
    pen.pensize(2)
    r = spacing / 3
    for y in range(rows):
        for x in range(cols):
            cx = ox + x * spacing
            cy = oy - y * spacing
            for angle in [0, 90, 180, 270]:
                pen.penup(); pen.goto(cx, cy)
                pen.setheading(angle); pen.forward(r)
                pen.pendown(); pen.circle(r, 180)

def kolam_diamond(rows, cols, spacing, ox, oy, color="maroon"):
    """Diamond grid pattern."""
    pen.color(color)
    pen.pensize(2)
    for y in range(rows - 1):
        for x in range(cols - 1):
            x1 = ox + x * spacing
            y1 = oy - y * spacing
            x2 = x1 + spacing
            y2 = y1 - spacing
            pen.penup(); pen.goto((x1 + x2) / 2, y1)
            pen.pendown(); pen.goto(x2, (y1 + y2) / 2)
            pen.goto((x1 + x2) / 2, y2)
            pen.goto(x1, (y1 + y2) / 2)
            pen.goto((x1 + x2) / 2, y1)

def kolam_snake(rows, cols, spacing, ox, oy, color="green"):
    """Snake-like continuous curve through grid."""
    pen.color(color)
    pen.pensize(2)
    r = spacing / 2.5
    for y in range(rows):
        cx = ox
        cy = oy - y * spacing
        pen.penup(); pen.goto(cx, cy); pen.pendown()
        for x in range(cols):
            pen.circle(r, 180)
            pen.forward(spacing / 2)

def kolam_combo(rows, cols, spacing, ox, oy):
    """Combination of loops + flowers."""
    kolam_loops(rows, cols, spacing, ox, oy, "black")
    kolam_flower(rows, cols, spacing, ox, oy, "red")

# ---------------- Controller ----------------
PATTERNS = {
    "Loop Kolam": kolam_loops,
    "Flower Kolam": kolam_flower,
    "Diamond Kolam": kolam_diamond,
    "Snake Kolam": kolam_snake,
    "Combination Kolam": kolam_combo,
}

def draw_pattern(name, rows, cols, spacing):
    reset_canvas(rows, cols, spacing)
    ox, oy = grid_offsets(rows, cols, spacing)
    draw_dot_grid(rows, cols, spacing, ox, oy)
    func = PATTERNS.get(name, kolam_loops)
    func(rows, cols, spacing, ox, oy)
    pen.penup(); pen.home(); pen.pendown()  # Reset cursor

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
root.title("Kolam Generator GUI")
root.geometry("400x300")

tk.Label(root, text="Rows:").grid(row=0, column=0, pady=6, sticky="e")
rows_entry = tk.Entry(root); rows_entry.insert(0, "5"); rows_entry.grid(row=0, column=1)

tk.Label(root, text="Cols:").grid(row=1, column=0, pady=6, sticky="e")
cols_entry = tk.Entry(root); cols_entry.insert(0, "5"); cols_entry.grid(row=1, column=1)

tk.Label(root, text="Spacing:").grid(row=2, column=0, pady=6, sticky="e")
spacing_entry = tk.Entry(root); spacing_entry.insert(0, "60"); spacing_entry.grid(row=2, column=1)

tk.Label(root, text="Pattern:").grid(row=3, column=0, pady=6, sticky="e")
pattern_var = tk.StringVar(value="Loop Kolam")
pattern_menu = ttk.Combobox(
    root, textvariable=pattern_var,
    values=list(PATTERNS.keys()), state="readonly", width=25
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
