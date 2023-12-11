import tkinter as tk

def move_object():
    canvas.move(rectangle, 5, 0)  # Move the object 5 pixels to the right
    root.after(50, move_object)   # Call move_object again after 50 milliseconds

root = tk.Tk()
root.title("Animated Object Movement")

canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# Create a rectangle (the object to be animated)
rectangle = canvas.create_rectangle(50, 50, 100, 100, fill="blue")

# Start the animation
move_object()

root.mainloop()
