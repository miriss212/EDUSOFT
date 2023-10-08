import tkinter as tk
from PIL import Image, ImageTk

# Function to change the size of the background picture
def change_background_size(new_width, new_height):
    global tk_image, canvas_background
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(background_item, image=tk_image)

# Function to be called when a button is clicked
def button_click(button_number):
    canvas.create_text(50, 50 + button_number * 30, text=f"Button {button_number} clicked!")

def reset():
    print("reset")

def switch_mode():
    global exp
    exp = not exp  # Toggle the mode (True to False, or False to True)
    update_button_text()  # Call the function to update button text

def update_button_text():
    if exp:
        button_mode.config(text="Experimental mode")
    else:
        button_mode.config(text="Test mode")

# Create the main application window
root = tk.Tk()
root.title("Canvas and Buttons Example")
exp = False  # Initialize the mode as False (Test mode)

# Open and convert the image to a suitable format
image = Image.open("C:/Users/cidom/OneDrive/Dokumenty/mAIN2/edusoft/sand.jpg")
tk_image = ImageTk.PhotoImage(image)

# Create a canvas widget
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Create a canvas item for the background image
background_item = canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

# Create a frame for the buttons and pack it at the top
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP)

# Create buttons to change the background size
button1 = tk.Button(button_frame, text="Resize to 200x200", command=lambda: change_background_size(200, 200))
button2 = tk.Button(button_frame, text="Resize to 400x300", command=lambda: change_background_size(400, 300))
button1.pack(side=tk.LEFT)
button2.pack(side=tk.LEFT)

# Create a button to switch between modes
button_mode = tk.Button(button_frame, text="", command=switch_mode)
update_button_text()  # Initialize the button text based on the initial mode
button_mode.pack(side=tk.LEFT)

# Create a button for the reset function
buttonRESET = tk.Button(button_frame, text="Reset", command=reset)
buttonRESET.pack(side=tk.LEFT)

# Start the main event loop
root.mainloop()
