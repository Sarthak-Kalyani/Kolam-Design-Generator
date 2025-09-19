import turtle

def setup_screen():
    """Sets up the turtle screen for drawing."""
    screen = turtle.Screen()
    screen.title("Geometric Pattern Generator")
    screen.bgcolor("black")
    turtle.speed(0) # Fastest drawing speed
    turtle.hideturtle()
    turtle.pensize(2)
    turtle.pencolor("white")

def draw_star_spiral(size, num_points, angle):
    """
    Draws a star spiral pattern.
    
    Args:
        size (int): The initial length of the first line segment.
        num_points (int): The number of points on the star (e.g., 5 for a pentagram).
        angle (int): The angle of rotation for the spiral effect.
    """
    # Calculate the inner angle of the star
    star_angle = 180 - (180 / num_points)
    
    for x in range(300):
        turtle.forward(size)
        turtle.right(star_angle + angle)
        size += 2 # Gradually increase the size of each line segment

def main():
    """Main function to run the geometric pattern generator."""
    setup_screen()
    
    # You can change these values to create different patterns!
    # A 5-pointed star, gradually spiraling out.
    draw_star_spiral(10, 5, 1) 
    
    turtle.done()

if __name__ == "__main__":
    main()


