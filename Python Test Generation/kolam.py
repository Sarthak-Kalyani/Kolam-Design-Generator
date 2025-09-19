import turtle
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

# Setup screen
screen = turtle.Screen()
screen.title("Kolam Generator")
screen.bgcolor("white")

pen = turtle.Turtle()
pen.speed(0)

# --- Kolam Functions ---
def draw_dot_grid(rows, cols, spacing, offset_x, offset_y):
    """Draw the basic dot grid"""
    for y in range(rows):
        for x in range(cols):
            pen.penup()
            pen.goto(offset_x + x * spacing, offset_y - y * spacing)
            pen.dot(6, "black")

def draw_kolam_loops(rows, cols, spacing, offset_x, offset_y, color="blue"):
    """Loops around each dot"""
    pen.pensize(2)
    pen.color(color)
    for y in range(rows):
        for x in range(cols):
            pen.penup()
            pen.goto(offset_x + x * spacing, offset_y - y * spacing)
            pen.pendown()
            for i in range(4):
                pen.circle(spacing/2, 180)
                pen.right(90)

def draw_kolam_lines(rows, cols, spacing, offset_x, offset_y, color="red"):
    """Lines connecting dots (grid style)"""
    pen.pensize(2)
    pen.color(color)
    for y in range(rows):
        for x in range(cols):
            x_pos = offset_x + x * spacing
            y_pos = offset_y - y * spacing
            if x < cols - 1:  # Horizontal line
                pen.penup(); pen.goto(x_pos, y_pos)
                pen.pendown(); pen.goto(offset_x + (x+1)*spacing, y_pos)
            if y < rows - 1:  # Vertical line
                pen.penup(); pen.goto(x_pos, y_pos)
                pen.pendown(); pen.goto(x_pos, offset_y - (y+1)*spacing)

def draw_circle_kolam(rows, cols, spacing, offset_x, offset_y, color="green"):
    """Draws circles around each dot"""
    pen.pensize(2)
    pen.color(color)
    for y in range(rows):
        for x in range(cols):
            pen.penup()
            pen.goto(offset_x + x * spacing, offset_y - y * spacing - spacing/2)
            pen.pendown()
            pen.circle(spacing/2)

def draw_spiral_kolam(rows, cols, spacing, offset_x, offset_y, color="purple"):
    """Spirals around each dot"""
    pen.pensize(2)
    pen.color(color)
    for y in range(rows):
        for x in range(cols):
            pen.penup()
            pen.goto(offset_x + x * spacing, offset_y - y * spacing)
            pen.pendown()
            for r in range(5, spacing, 5):
                pen.circle(r, 90)

# --- Main Drawing Function ---
def draw_pattern(pattern, rows, cols, spacing):
    pen.clear()
    pen.penup()

    total_width = (cols - 1) * spacing + 200
    total_height = (rows - 1) * spacing + 200
    screen.setup(width=total_width, height=total_height)

    offset_x = -((cols - 1) * spacing) / 2
    offset_y = ((rows - 1) * spacing) / 2

    draw_dot_grid(rows, cols, spacing, offset_x, offset_y)

    if pattern == "Loops":
        draw_kolam_loops(rows, cols, spacing, offset_x, offset_y)
    elif pattern == "Lines":
        draw_kolam_lines(rows, cols, spacing, offset_x, offset_y)
    elif pattern == "Circles":
        draw_circle_kolam(rows, cols, spacing, offset_x, offset_y)
    elif pattern == "Spirals":
        draw_spiral_kolam(rows, cols, spacing, offset_x, offset_y)

# --- Save Function (PNG/JPG only) ---
def save_as_image():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg")]
    )
    if file_path:
        try:
            canvas = screen.getcanvas()
            canvas.postscript(file="temp.eps", colormode="color")

            img = Image.open("temp.eps")
            if file_path.endswith(".jpg"):
                img = img.convert("RGB")  # JPG fix
            img.save(file_path, dpi=(300, 300))

            messagebox.showinfo("Saved", f"✅ Kolam saved at {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Saving failed.\n{e}")

# --- GUI (Tkinter) ---
root = tk.Tk()
root.title("Kolam Generator GUI")
root.geometry("350x250")

tk.Label(root, text="Rows:").grid(row=0, column=0, pady=5, sticky="e")
rows_entry = tk.Entry(root); rows_entry.insert(0, "5"); rows_entry.grid(row=0, column=1)

tk.Label(root, text="Cols:").grid(row=1, column=0, pady=5, sticky="e")
cols_entry = tk.Entry(root); cols_entry.insert(0, "5"); cols_entry.grid(row=1, column=1)

tk.Label(root, text="Spacing:").grid(row=2, column=0, pady=5, sticky="e")
spacing_entry = tk.Entry(root); spacing_entry.insert(0, "50"); spacing_entry.grid(row=2, column=1)

tk.Label(root, text="Pattern:").grid(row=3, column=0, pady=5, sticky="e")
pattern_var = tk.StringVar(value="Loops")
pattern_menu = ttk.Combobox(root, textvariable=pattern_var,
                            values=["Loops", "Lines", "Circles", "Spirals"])
pattern_menu.grid(row=3, column=1)

def run_drawing():
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    spacing = int(spacing_entry.get())
    pattern = pattern_menu.get()
    draw_pattern(pattern, rows, cols, spacing)

tk.Button(root, text="Draw Kolam", command=run_drawing, bg="lightblue").grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Save Kolam", command=save_as_image, bg="lightgreen").grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()
