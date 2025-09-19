import turtle
import tkinter as tk
from tkinter import ttk

# ---------- Kolam Design Functions ----------

def reset_turtle():
    turtle.reset()
    turtle.speed(0)
    turtle.bgcolor("white")
    turtle.pencolor("black")
    turtle.hideturtle()

def diamond_kolam():
    reset_turtle()
    size = 40
    for i in range(12):
        turtle.penup()
        turtle.goto(0, 0)
        turtle.forward(size * i)
        turtle.pendown()
        for _ in range(4):
            turtle.forward(size)
            turtle.right(90)

def square_kolam():
    reset_turtle()
    size = 50
    for i in range(36):
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()
        turtle.forward(size)
        turtle.right(100)

def lotus_centre():
    reset_turtle()
    turtle.penup()
    turtle.goto(0, -100)   # centered lotus
    turtle.pendown()
    for i in range(36):
        turtle.circle(100, steps=6)
        turtle.right(170)

def snake_kolam():
    reset_turtle()
    size = 20
    for i in range(60):
        turtle.circle(size, 180)
        turtle.circle(-size, 180)

def infinity_cells():
    reset_turtle()
    size = 60
    for i in range(18):
        turtle.circle(size, 90)
        turtle.circle(-size, 90)
        turtle.right(20)

def spiral_kolam():
    reset_turtle()
    for i in range(80):
        turtle.circle(i*2, 90)

def star_kolam():
    reset_turtle()
    size = 200
    for i in range(36):
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
