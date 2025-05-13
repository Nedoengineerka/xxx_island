import tkinter as tk
from src.hexagon_grid import HexagonGrid

# Create the main window
root = tk.Tk()
root.title('Reap what you sow event simulation')

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to a wide screen format
root.geometry(f'{screen_width}x{screen_height}')

# Set minimum window size
root.minsize(600, 600)

# Create the grid
hex_grid = HexagonGrid(root)

# Run the application
root.mainloop() 