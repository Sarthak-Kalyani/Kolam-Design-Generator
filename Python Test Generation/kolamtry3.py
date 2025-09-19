import turtle

def draw_diamond_grid(rows, cols, spacing=40):
    turtle.speed(0)
    turtle.hideturtle()
    turtle.bgcolor("black")
    turtle.color("white")

    start_x = - (cols - 1) * spacing // 2
    start_y = (rows - 1) * spacing // 2

    dots = []  # store dot positions
    for r in range(rows):
        row_dots = []
        for c in range(cols):
            x = start_x + c * spacing + (r * spacing // 2)
            y = start_y - r * spacing
            turtle.penup()
            turtle.goto(x, y)
            turtle.pendown()
            turtle.dot(8, "white")
            row_dots.append((x, y))
        dots.append(row_dots)
    return dots


def draw_square_loop(dots, spacing=40):
    turtle.color("yellow")
    turtle.pensize(2)

    for r in range(len(dots)-1):
        for c in range(len(dots[r])-1):
            # get 4 dots (square block)
            x1, y1 = dots[r][c]
            x2, y2 = dots[r][c+1]
            x3, y3 = dots[r+1][c]
            x4, y4 = dots[r+1][c+1]

            # draw a loop around them
            turtle.penup()
            turtle.goto((x1+x2)/2, y1+spacing/3)
            turtle.pendown()
            turtle.circle(spacing/2, 90)
            turtle.goto((x2+x4)/2 + spacing/3, (y2+y4)/2)
            turtle.circle(spacing/2, 90)
            turtle.goto((x3+x4)/2, y3-spacing/3)
            turtle.circle(spacing/2, 90)
            turtle.goto((x1+x3)/2 - spacing/3, (y1+y3)/2)
            turtle.circle(spacing/2, 90)


# MAIN
dots = draw_diamond_grid(7, 7, 40)
draw_square_loop(dots, 40)

turtle.done()
