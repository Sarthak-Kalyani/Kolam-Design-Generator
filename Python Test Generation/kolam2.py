import turtle
import tkinter as tk
from tkinter import ttk

# --- Setup ---
screen = turtle.Screen()
screen.title("Kolam Generator")
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.pensize(2)
pen.hideturtle()

# --- Helpers ---
def draw_dot(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.begin_fill()
    pen.circle(3)
    pen.end_fill()

def reset_canvas(rows, cols, spacing):
    pen.clear()
    total_width = (cols - 1) * spacing + 200
    total_height = (rows - 1) * spacing + 200
    screen.setup(width=total_width, height=total_height)

def make_grid(rows, cols, spacing):
    dots = []
    for i in range(-(rows//2), rows//2+1):
        for j in range(-(cols//2), cols//2+1):
            draw_dot(i*spacing, j*spacing)
            dots.append((i*spacing, j*spacing))
    return dots

# --- Kolam Patterns ---
def kolam_lotus(rows, cols, spacing):
    dots = make_grid(rows, cols, spacing)
    for (x, y) in dots:
        for angle in [0, 90, 180, 270]:
            pen.penup()
            pen.goto(x, y)
            pen.setheading(angle)
            pen.forward(spacing/2)
            pen.pendown()
            pen.circle(spacing/2, 180)

def kolam_butterfly(rows, cols, spacing):
    dots = make_grid(rows, cols, spacing)
    for (x, y) in dots:
        pen.penup()
        pen.goto(x, y - spacing/2)
        pen.setheading(0)
        pen.pendown()
        pen.circle(spacing/2, 180)
        pen.circle(-spacing/2, 180)

def kolam_star(rows, cols, spacing):
    dots = make_grid(rows, cols, spacing)
    size = spacing * 0.6
    for (x, y) in dots:
        pen.penup()
        pen.goto(x, y - size/2)
        pen.setheading(90)
        pen.pendown()
        for _ in range(5):
            pen.forward(size)
            pen.right(144)

def kolam_diamond(rows, cols, spacing):
    dots = make_grid(rows, cols, spacing)
    for (x, y) in dots:
        pen.penup()
        pen.goto(x - spacing/2, y)
        pen.pendown()
        pen.goto(x, y + spacing/2)
        pen.goto(x + spacing/2, y)
        pen.goto(x, y - spacing/2)
        pen.goto(x - spacing/2, y)

def kolam_loops(rows, cols, spacing):
    dots = make_grid(rows, cols, spacing)
    for (x, y) in dots:
        pen.penup()
        pen.goto(x, y)
        pen.setheading(0)
        pen.forward(spacing/2)
        pen.right(90)
        pen.pendown()
        for _ in range(4):
            pen.circle(spacing/2, 180)
            pen.right(90)

# --- Controller ---
PATTERNS = {
    "Lotus Kolam 🌸": kolam_lotus,
    "Butterfly Kolam 🦋": kolam_butterfly,
    "Star Kolam ✨": kolam_star,
    "Diamond Kolam 🔷": kolam_diamond,
    "Concentric Loops 🔄": kolam_loops
}

def draw_pattern(name, rows, cols, spacing):
    reset_canvas(rows, cols, spacing)
    func = PATTERNS.get(name, kolam_lotus)
    func(rows, cols, spacing)
    pen.penup()
    pen.home()  # reset cursor to center

# --- GUI ---
root = tk.Tk()
root.title("Kolam Generator")
root.geometry("400x250")

tk.Label(root, text="Rows:").grid(row=0, column=0, pady=5)
rows_entry = tk.Entry(root)
rows_entry.insert(0, "5")
rows_entry.grid(row=0, column=1)

tk.Label(root, text="Cols:").grid(row=1, column=0, pady=5)
cols_entry = tk.Entry(root)
cols_entry.insert(0, "5")
cols_entry.grid(row=1, column=1)

tk.Label(root, text="Spacing:").grid(row=2, column=0, pady=5)
spacing_entry = tk.Entry(root)
spacing_entry.insert(0, "60")
spacing_entry.grid(row=2, column=1)

tk.Label(root, text="Pattern:").grid(row=3, column=0, pady=5)
pattern_var = tk.StringVar(value="Lotus Kolam 🌸")
pattern_menu = ttk.Combobox(root, textvariable=pattern_var,
                            values=list(PATTERNS.keys()), state="readonly", width=25)
pattern_menu.grid(row=3, column=1)

def run_drawing():
    try:
        rows = max(2, int(rows_entry.get()))
        cols = max(2, int(cols_entry.get()))
        spacing = max(20, int(spacing_entry.get()))
    except Exception:
        return
    draw_pattern(pattern_menu.get(), rows, cols, spacing)

tk.Button(root, text="Draw Kolam", command=run_drawing, bg="lightblue").grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
