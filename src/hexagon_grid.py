import tkinter as tk
import math

class HexagonGrid:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Constants for hexagon size and spacing
        self.hex_size = 30  # Distance from center to corner
        
        # Store existing hexagons (center positions) and buttons
        self.hexagons = set()
        self.buttons = {}  # Maps button id to target position for new hexagon
        
        # Wait for window to be ready before drawing
        self.root.update()
        self.draw_initial_hexagon()
        
        # Bind window resize event
        self.root.bind('<Configure>', self.on_resize)
    
    def get_hexagon_points(self, center_x, center_y):
        """Calculate the 6 corner points of a hexagon."""
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center_x + self.hex_size * math.cos(angle)
            y = center_y + self.hex_size * math.sin(angle)
            points.extend([x, y])
        return points
    
    def draw_hexagon(self, center_x, center_y):
        """Draw a hexagon at the specified center position."""
        points = self.get_hexagon_points(center_x, center_y)
        self.canvas.create_polygon(points, fill='white', outline='black', width=1)
        self.hexagons.add((center_x, center_y))
        self.add_plus_buttons(center_x, center_y)
    
    def add_plus_buttons(self, hex_x, hex_y):
        """Add plus buttons at the midpoint of each side of the hexagon."""
        for i in range(6):
            # Calculate the side midpoint
            angle1 = i * math.pi / 3
            angle2 = ((i + 1) % 6) * math.pi / 3
            
            # Get the corners of this side
            x1 = hex_x + self.hex_size * math.cos(angle1)
            y1 = hex_y + self.hex_size * math.sin(angle1)
            x2 = hex_x + self.hex_size * math.cos(angle2)
            y2 = hex_y + self.hex_size * math.sin(angle2)
            
            # Calculate the exact middle of the side
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Calculate the adjacent hexagon position
            # For a flat-topped hexagon, the distance between centers of adjacent hexagons is 2*radius
            # Where radius is the distance from center to a corner
            shift_angle = (angle1 + angle2) / 2  # Midpoint angle
            new_hex_x = hex_x + 2 * self.hex_size * math.cos(shift_angle)
            new_hex_y = hex_y + 2 * self.hex_size * math.sin(shift_angle)
            
            # Check if there is already a hexagon at this position
            if not self.is_position_occupied(new_hex_x, new_hex_y):
                # Create the plus button on the middle of the side
                button = self.canvas.create_text(
                    mid_x, mid_y,
                    text="+",
                    font=('Arial', 10, 'bold'),
                    tags=('button',)
                )
                self.buttons[button] = (new_hex_x, new_hex_y)
        
        self.canvas.tag_bind('button', '<Button-1>', self.on_plus_click)
    
    def is_position_occupied(self, x, y):
        """Check if there is already a hexagon at or very near the specified position."""
        for hx, hy in self.hexagons:
            # Use a smaller threshold for more accurate position checking
            if abs(x - hx) < self.hex_size * 0.1 and abs(y - hy) < self.hex_size * 0.1:
                return True
        return False
    
    def on_plus_click(self, event):
        """Handle click on a plus button."""
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        if clicked_item in self.buttons:
            new_x, new_y = self.buttons[clicked_item]
            # Remove the clicked button
            self.canvas.delete(clicked_item)
            del self.buttons[clicked_item]
            # Draw new hexagon
            self.draw_hexagon(new_x, new_y)
            # Update all buttons to reflect the new state
            self.update_all_buttons()
    
    def update_all_buttons(self):
        """Update all plus buttons based on current hexagons."""
        # Clear all existing buttons
        for button in list(self.buttons.keys()):
            self.canvas.delete(button)
        self.buttons.clear()
        
        # Redraw buttons for all hexagons
        for hex_x, hex_y in self.hexagons:
            self.add_plus_buttons(hex_x, hex_y)
    
    def draw_initial_hexagon(self):
        """Draw the initial hexagon in the center of the window."""
        # Get the current window dimensions
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Calculate the center position
        self.center_x = window_width // 2
        self.center_y = window_height // 2
        
        # Clear any existing hexagons and buttons
        self.canvas.delete("all")
        self.hexagons.clear()
        self.buttons.clear()
        
        # Draw the hexagon at the center
        self.draw_hexagon(self.center_x, self.center_y)
    
    def on_resize(self, event):
        """Handle window resize event."""
        # Only redraw if the window size actually changed significantly
        if abs(event.width - self.root.winfo_width()) > 20 or abs(event.height - self.root.winfo_height()) > 20:
            self.draw_initial_hexagon() 