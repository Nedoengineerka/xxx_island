import tkinter as tk

# Create the main window
root = tk.Tk()
root.title('Hello World App')

# Define the button click event
def on_button_click():
    print('Hello, World!')

# Create a button widget
hello_button = tk.Button(root, text='Hello World', command=on_button_click)
hello_button.pack(pady=20)

# Run the application
root.mainloop() 