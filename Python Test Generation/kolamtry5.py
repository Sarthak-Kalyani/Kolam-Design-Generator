import matplotlib.pyplot as plt
import numpy as np
import math

class KolamGenerator:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.fig, self.ax = plt.subplots(figsize=(width, height))
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_facecolor('black')  # Traditional kolam background
    
    def draw_dot_grid(self, spacing=1, dot_size=20):
        """Draw the traditional dot grid that guides kolam patterns"""
        for x in np.arange(0.5, self.width, spacing):
            for y in np.arange(0.5, self.height, spacing):
                self.ax.plot(x, y, 'o', color='white', markersize=dot_size/10, alpha=0.3)
    
    def draw_curved_line(self, start, end, control_points, color='white', linewidth=3):
        """Draw smooth curved lines between points"""
        points = [start] + control_points + [end]
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        
        # Create smooth curve using spline interpolation
        t = np.linspace(0, 1, 100)
        x_smooth = np.interp(t, np.linspace(0, 1, len(x_coords)), x_coords)
        y_smooth = np.interp(t, np.linspace(0, 1, len(y_coords)), y_coords)
        
        self.ax.plot(x_smooth, y_smooth, color=color, linewidth=linewidth)
    
    def save_kolam(self, filename):
        """Save the kolam design"""
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.show()

def generate_lotus_kolam():
    """Generate a traditional lotus kolam pattern"""
    kolam = KolamGenerator(12, 12)
    kolam.draw_dot_grid(spacing=1)
    
    center_x, center_y = 6, 6
    
    # Draw lotus petals
    for i in range(8):
        angle = i * 2 * math.pi / 8
        
        # Petal outer curve
        start = (center_x, center_y)
        end_x = center_x + 3 * math.cos(angle)
        end_y = center_y + 3 * math.sin(angle)
        
        # Control points for petal shape
        ctrl1_x = center_x + 1.5 * math.cos(angle - 0.3)
        ctrl1_y = center_y + 1.5 * math.sin(angle - 0.3)
        ctrl2_x = center_x + 2.5 * math.cos(angle)
        ctrl2_y = center_y + 2.5 * math.sin(angle)
        
        kolam.draw_curved_line(start, (end_x, end_y), 
                              [(ctrl1_x, ctrl1_y), (ctrl2_x, ctrl2_y)], 
                              color='#FFD700')
        
        # Return curve for petal
        ctrl3_x = center_x + 1.5 * math.cos(angle + 0.3)
        ctrl3_y = center_y + 1.5 * math.sin(angle + 0.3)
        
        kolam.draw_curved_line((end_x, end_y), start, 
                              [(ctrl2_x, ctrl2_y), (ctrl3_x, ctrl3_y)], 
                              color='#FFD700')
    
    # Center circle
    circle = plt.Circle((center_x, center_y), 0.5, 
                       color='#FF6B6B', fill=True)
    kolam.ax.add_patch(circle)
    
    kolam.save_kolam('lotus_kolam.png')

def generate_geometric_kolam():
    """Generate a geometric kolam with interlocking patterns"""
    kolam = KolamGenerator(10, 10)
    kolam.draw_dot_grid(spacing=0.8)
    
    center_x, center_y = 5, 5
    
    # Draw concentric squares with curves
    for size in [1, 2, 3, 4]:
        # Four sides of square with curved connections
        corners = [
            (center_x - size, center_y - size),
            (center_x + size, center_y - size),
            (center_x + size, center_y + size),
            (center_x - size, center_y + size)
        ]
        
        for i in range(4):
            start = corners[i]
            end = corners[(i + 1) % 4]
            
            # Create curved connection between corners
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            
            # Curve outward from center
            offset = 0.3 * size
            if i % 2 == 0:  # horizontal sides
                ctrl = (mid_x, mid_y + offset * ((1 if i == 0 else -1)))
            else:  # vertical sides
                ctrl = (mid_x + offset * ((1 if i == 1 else -1)), mid_y)
            
            color = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'][size-1]
            kolam.draw_curved_line(start, end, [ctrl], color=color)
    
    kolam.save_kolam('geometric_kolam.png')

def generate_flower_chain_kolam():
    """Generate a kolam with connected flower motifs"""
    kolam = KolamGenerator(15, 10)
    kolam.draw_dot_grid(spacing=0.7)
    
    # Create a chain of flowers
    flower_centers = [(3, 5), (7.5, 5), (12, 5)]
    
    for center_x, center_y in flower_centers:
        # Draw flower petals
        for i in range(6):
            angle = i * 2 * math.pi / 6
            
            # Petal endpoints
            petal_x = center_x + 1.5 * math.cos(angle)
            petal_y = center_y + 1.5 * math.sin(angle)
            
            # Create petal shape with two curves
            ctrl1_x = center_x + 0.8 * math.cos(angle - 0.5)
            ctrl1_y = center_y + 0.8 * math.sin(angle - 0.5)
            ctrl2_x = center_x + 0.8 * math.cos(angle + 0.5)
            ctrl2_y = center_y + 0.8 * math.sin(angle + 0.5)
            
            # Draw petal
            kolam.draw_curved_line((center_x, center_y), (petal_x, petal_y), 
                                  [(ctrl1_x, ctrl1_y)], color='#E74C3C')
            kolam.draw_curved_line((petal_x, petal_y), (center_x, center_y), 
                                  [(ctrl2_x, ctrl2_y)], color='#E74C3C')
        
        # Flower center
        circle = plt.Circle((center_x, center_y), 0.3, 
                           color='#F39C12', fill=True)
        kolam.ax.add_patch(circle)
    
    # Connect flowers with decorative curves
    for i in range(len(flower_centers) - 1):
        start = flower_centers[i]
        end = flower_centers[i + 1]
        
        # Create connecting vine
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        
        kolam.draw_curved_line(start, end, 
                              [(mid_x, mid_y + 1), (mid_x, mid_y - 1)], 
                              color='#27AE60', linewidth=2)
    
    kolam.save_kolam('flower_chain_kolam.png')

def generate_spiral_kolam():
    """Generate a spiral-based kolam pattern"""
    kolam = KolamGenerator(12, 12)
    kolam.draw_dot_grid(spacing=0.6)
    
    center_x, center_y = 6, 6
    
    # Create multiple spirals
    for spiral_num in range(4):
        points = []
        start_angle = spiral_num * math.pi / 2
        
        for t in np.linspace(0, 4 * math.pi, 50):
            radius = 0.1 + t * 0.3
            x = center_x + radius * math.cos(t + start_angle)
            y = center_y + radius * math.sin(t + start_angle)
            points.append((x, y))
        
        # Draw spiral as connected curves
        colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12']
        for i in range(len(points) - 3):
            kolam.draw_curved_line(points[i], points[i+2], 
                                  [points[i+1]], 
                                  color=colors[spiral_num], linewidth=2)
    
    kolam.save_kolam('spiral_kolam.png')

def main():
    """Generate all kolam patterns"""
    print("🌸 Generating Traditional Kolam Designs...")
    
    print("Creating Lotus Kolam...")
    generate_lotus_kolam()
    
    print("Creating Geometric Kolam...")
    generate_geometric_kolam()
    
    print("Creating Flower Chain Kolam...")
    generate_flower_chain_kolam()
    
    print("Creating Spiral Kolam...")
    generate_spiral_kolam()
    
    print("✨ All kolam designs generated successfully!")
    print("Check your directory for PNG files.")

if __name__ == "__main__":
    main()

def interactive_kolam_designer():
    """Interactive kolam pattern designer"""
    print("🎨 Interactive Kolam Designer")
    print("Choose a pattern to generate:")
    print("1. Lotus Kolam")
    print("2. Geometric Kolam")
    print("3. Flower Chain Kolam")
    print("4. Spiral Kolam")
    print("5. Generate All Patterns")
    
    choice = input("Enter your choice (1-5): ")
    
    if choice == "1":
        generate_lotus_kolam()
    elif choice == "2":
        generate_geometric_kolam()
    elif choice == "3":
        generate_flower_chain_kolam()
    elif choice == "4":
        generate_spiral_kolam()
    elif choice == "5":
        main()
    else:
        print("Invalid choice! Please run again.")

# Uncomment to run interactive designer
# interactive_kolam_designer()