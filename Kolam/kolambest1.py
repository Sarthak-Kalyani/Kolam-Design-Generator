import turtle

# Screen setup
screen = turtle.Screen()
screen.title("Lotus Kolam")
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

# Dot grid (5x5 square)
spacing = 50
dots = []
for i in range(-2, 3):
    for j in range(-2, 3):
        draw_dot(i*spacing, j*spacing)
        dots.append((i*spacing, j*spacing))

# Lotus petals around each dot
for (x, y) in dots:
    for angle in [0, 90, 180, 270]:
        pen.penup()
        pen.goto(x, y)
        pen.setheading(angle)
        pen.forward(spacing/2)
        pen.pendown()
        pen.circle(spacing/2, 180)

pen.hideturtle()
screen.mainloop()
