import turtle

# Setup
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Simple Diamond Kolam")
t = turtle.Turtle()
t.speed(0)
t.pensize(2)

# Grid size
CELL = 40
DOT_SIZE = 6
GRID = 4   # 4x4 diamond kolam

# -----------------------------
# Draw dot grid (diamond shape)
def draw_dot_grid():
    t.color("black")
    for row in range(GRID):
        for col in range(GRID):
            x = col * CELL - (GRID-1)*CELL/2
            y = row * CELL - (GRID-1)*CELL/2
            t.penup()
            t.goto(x, y)
            t.pendown()
            t.dot(DOT_SIZE, "black")

# -----------------------------
# Draw diamond kolam loops
def draw_kolam():
    t.color("blue")
    # Outer diamond loop
    t.penup()
    t.goto(-CELL*1.5, 0)
    t.pendown()
    t.setheading(45)
    for _ in range(4):
        t.circle(CELL*1.5, 90)

    # Inner square loop
    t.penup()
    t.goto(-CELL, 0)
    t.pendown()
    t.setheading(45)
    for _ in range(4):
        t.circle(CELL, 90)

# -----------------------------
# Run
draw_dot_grid()
draw_kolam()

t.hideturtle()
screen.mainloop()
