import turtle

# Screen setup
screen = turtle.Screen()
screen.title("Diamond Kolam")
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.pensize(2)

def draw_dot(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.begin_fill()
    pen.circle(3)
    pen.end_fill()

# Dot grid (5x5 diamond style)
spacing = 40
dots = []
for i in range(-2, 3):
    for j in range(-2, 3):
        if abs(i) + abs(j) <= 2:  # diamond shape
            draw_dot(i*spacing, j*spacing)
            dots.append((i*spacing, j*spacing))

# Draw loops around dots
for (x, y) in dots:
    pen.penup()
    pen.goto(x - spacing/2, y)
    pen.setheading(0)
    pen.pendown()
    pen.circle(spacing/2, 360)

pen.hideturtle()
screen.mainloop()
