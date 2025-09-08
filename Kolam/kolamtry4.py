import turtle
import tkinter as tk
from tkinter import ttk

# ---------- Kolam Design Functions ----------

def reset_turtle():
    turtle.reset()
    turtle.speed(0)
    turtle.bgcolor("black")
    turtle.pencolor("white")
    turtle.hideturtle()

def diamond_kolam():
    reset_turtle()
    size = 50
    turtle.penup()
    turtle.goto(-150, 150)   # center it better
    turtle.pendown()
    for i in range(12):
        for _ in range(4):
            turtle.forward(size)
            turtle.right(90)
        turtle.forward(size)

def square_kolam():
    reset_turtle()
    size = 120   # bigger
    for i in range(72):      # more turns → fuller pattern
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()
        turtle.forward(size)
        turtle.right(100)

def lotus_centre():
    reset_turtle()
    turtle.penup()
    turtle.goto(0, -150)   # properly centered lotus
    turtle.pendown()
    for i in range(36):
        turtle.circle(150, steps=6)
        turtle.right(170)

def snake_kolam():
    reset_turtle()
    size = 40
    for i in range(40):
        turtle.circle(size, 180)
        turtle.circle(-size, 180)

def infinity_cells():
    reset_turtle()
    size = 100
    for i in range(24):
        turtle.circle(size, 90)
        turtle.circle(-size, 90)
        turtle.right(15)

def spiral_kolam():
    reset_turtle()
    for i in range(100):
        turtle.circle(i * 3, 90)

def star_kolam():
    reset_turtle()
    size = 250
    for i in range(72):
        turtle.forward(size)
        turtle.right(170)

# ---------- Tkinter GUI ----------

def run_selected_pattern():
    pattern = pattern_combo.get()
    if pattern == "Diamond Kolam":
        diamond_kolam()
    elif pattern == "Square Kolam":
        square_kolam()
    elif pattern == "Lotus (Centre)":
        lotus_centre()
    elif pattern == "Snake Kolam":
        snake_kolam()
    elif pattern == "Infinity Cells":
        infinity_cells()
    elif pattern == "Spiral Kolam":
        spiral_kolam()
    elif pattern == "Star Kolam":
        star_kolam()

# ---------- Main Window ----------
root = tk.Tk()
root.title("Kolam Generator")

label = tk.Label(root, text="Select Kolam Pattern:", font=("Arial", 12))
label.pack(pady=10)

pattern_combo = ttk.Combobox(root, values=[
    "Diamond Kolam",
    "Square Kolam",
    "Lotus (Centre)",
    "Snake Kolam",
    "Infinity Cells",
    "Spiral Kolam",
    "Star Kolam"
], font=("Arial", 11))
pattern_combo.pack(pady=5)

btn = tk.Button(root, text="Generate Kolam", command=run_selected_pattern, font=("Arial", 12), bg="white")
btn.pack(pady=15)

root.mainloop()
