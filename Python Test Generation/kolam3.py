import turtle
import tkinter as tk
from tkinter import ttk

screen = turtle.Screen()
screen.title("Diamond-Style Kolam Generator")
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.pensize(2)
pen.hideturtle()

def draw_dot(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.begin_fill()
    pen.circle(3)
    pen.end_fill()

def reset_canvas(size, count):
    pen.clear()
    w = (count - 1) * size + 200
    h = (count - 1) * size + 200
    screen.setup(width=w, height=h)

def make_grid(size, count):
    dots = []
    offset = (count - 1) * size / 2
    for i in range(count):
        for j in range(count):
            x = i * size - offset
            y = offset - j * size
            draw_dot(x, y)
            dots.append((x, y))
    return dots

def kolam_diamond_star(size, count):
    dots = make_grid(size, count)
    for x, y in dots:
        # diamond
        pen.penup(); pen.goto(x - size/2, y)
        pen.pendown()
        pen.goto(x, y + size/2); pen.goto(x + size/2, y)
        pen.goto(x, y - size/2); pen.goto(x - size/2, y)
        # diagonal star lines
        pen.penup(); pen.goto(x - size/2, y - size/2); pen.pendown()
        pen.goto(x + size/2, y + size/2)
        pen.penup(); pen.goto(x - size/2, y + size/2); pen.pendown()
        pen.goto(x + size/2, y - size/2)

def kolam_multi_layer(size, count):
    dots = make_grid(size, count)
    for x, y in dots:
        for r in [size/2, size/3]:
            pen.penup(); pen.goto(x, y - r)
            pen.pendown(); pen.circle(r)

def kolam_maze_diamond(size, count):
    dots = make_grid(size, count)
    for x, y in dots:
        pen.penup(); pen.goto(x - size/2, y)
        pen.setheading(0)
        pen.pendown()
        for _ in range(4):
            pen.circle(size/2, 180)
            pen.right(90)

def kolam_simple_diamond(size, count):
    dots = make_grid(size, count)
    for x, y in dots:
        pen.penup(); pen.goto(x - size/2, y)
        pen.pendown()
        pen.goto(x, y + size/2); pen.goto(x + size/2, y)
        pen.goto(x, y - size/2); pen.goto(x - size/2, y)

PATTERNS = {
    "Diamond + Star": kolam_diamond_star,
    "Multi-Layer Diamond": kolam_multi_layer,
    "Maze Diamond": kolam_maze_diamond,
    "Simple Diamond": kolam_simple_diamond
}

def draw_pattern(name, size, count):
    reset_canvas(size, count)
    func = PATTERNS.get(name, kolam_simple_diamond)
    func(size, count)
    pen.penup(); pen.home()

# GUI
root = tk.Tk()
root.title("Kolam Patterns")
root.geometry("350x220")

tk.Label(root, text="Grid Size:").grid(row=0, column=0, pady=5)
size_entry = tk.Entry(root); size_entry.insert(0, "60"); size_entry.grid(row=0, column=1)

tk.Label(root, text="Dot Count:").grid(row=1, column=0, pady=5)
count_entry = tk.Entry(root); count_entry.insert(0, "5"); count_entry.grid(row=1, column=1)

tk.Label(root, text="Pattern:").grid(row=2, column=0, pady=5)
pattern_var = tk.StringVar(value="Diamond + Star")
pattern_menu = ttk.Combobox(root, textvariable=pattern_var, values=list(PATTERNS.keys()), state="readonly", width=20)
pattern_menu.grid(row=2, column=1)

def run_draw():
    try:
        size = max(20, int(size_entry.get()))
        count = max(3, int(count_entry.get()))
    except:
        return
    draw_pattern(pattern_menu.get(), size, count)

tk.Button(root, text="Draw Kolam", command=run_draw, bg="lightgreen").grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
