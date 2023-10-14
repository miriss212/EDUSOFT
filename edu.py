import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

class MapEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Jedným ťahom")

        self.mode = "normal"  # Initial mode is normal
        

        # Open a JPEG image and convert it to PhotoImage
        self.background_image = self.load_and_resize_image("c:\\Users\\cidom\\OneDrive\\Dokumenty\\mAIN2\\edusoft\\sand.jpg", 400, 400)

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)  # Set the image as the background
        self.canvas.grid(row=1, column=0, columnspan=4)

        self.mode_label = tk.Label(root, text="Mode: " + self.mode, bg="sandybrown")
        self.mode_label.grid(row=0, column=0, columnspan=4)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.grid(row=2, column=0, columnspan=5)

        self.switch_button = tk.Button(self.buttons_frame, text="Switch Mode", command=self.toggle_mode, bg='sandybrown')
        self.switch_button.grid(row=0, column=0, padx=5, pady=5)

        self.save_button = tk.Button(self.buttons_frame, text="Save Map", command=self.save_map, bg='sandybrown')
        self.open_button = tk.Button(self.buttons_frame, text="Open Map", command=self.open_map, bg='sandybrown')
        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_map, bg='sandybrown')
        self.try_button = tk.Button(self.buttons_frame, text="Try Map", command=self.try_map, bg='sandybrown')
        self.no_solution_button = tk.Button(self.buttons_frame, text="No Solution", command=self.no_solution, bg='sandybrown')

        self.save_button.grid(row=0, column=1, padx=5, pady=5)
        self.open_button.grid(row=0, column=2, padx=5, pady=5)
        self.reset_button.grid(row=0, column=3, padx=5, pady=5)
        self.try_button.grid(row=0, column=4, padx=5, pady=5)
        self.no_solution_button.grid(row=0, column=5, padx=5, pady=5)

        self.create_size_slider()

        self.set_button_states()  # Set initial button states

    def load_and_resize_image(self, path, width, height):
        original_image = Image.open(path)
        resized_image = original_image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def toggle_mode(self):
        self.mode = "experimental" if self.mode == "normal" else "normal"
        self.set_button_states()
        self.mode_label.config(text="Mode: " + self.mode)

    def set_button_states(self):
        if self.mode == "normal":
            self.save_button.grid_forget()
            self.open_button.grid(row=0, column=1)
            self.reset_button.grid(row=0, column=2)
            self.try_button.grid_forget()
            self.size_label.grid_forget()
            self.size_slider.grid_forget()
            self.submit_resize_button.grid_forget()
            self.no_solution_button.grid(row=0, column=4, padx=5, pady=5)
        else:
            self.save_button.grid(row=0, column=1)
            self.open_button.grid_forget()
            self.reset_button.grid(row=0, column=2)
            self.try_button.grid(row=0, column=3)
            self.size_label.grid(row=1, column=1, padx=5, pady=5)
            self.size_slider.grid(row=1, column=2, padx=5, pady=5)
            self.submit_resize_button.grid(row=1, column=3, padx=5, pady=5)
            self.no_solution_button.grid_forget()

    def create_size_slider(self):
        self.size_label = tk.Label(self.buttons_frame, text="Set Size:", bg="sandybrown")
        self.size_slider = tk.Scale(self.buttons_frame, from_=100, to=500, orient="horizontal", length=200, bg='#ffc299', highlightbackground='#ff6600')
        self.size_slider.set(400)
        self.size_label.grid(row=1, column=1, padx=5, pady=5)
        self.size_slider.grid(row=1, column=2, padx=5, pady=5)
        self.submit_resize_button = tk.Button(self.buttons_frame, text="Submit Resize", command=self.submit_resize, bg='sandybrown')

    def submit_resize(self):
        new_size = self.size_slider.get()
        self.resize_canvas(new_size, new_size)

    def resize_canvas(self, width, height):
        self.canvas.config(width=width, height=height)
        self.background_image = self.load_and_resize_image("c:\\Users\\cidom\\OneDrive\\Dokumenty\\mAIN2\\edusoft\\sand.jpg", width, height)
        self.canvas.itemconfig(1, image=self.background_image)

    def save_map(self):
        # Add code to save the map in experimental mode
        pass

    def open_map(self):
        # Add code to open a saved map in normal mode
        pass

    def reset_map(self):
        # Add code to reset the map
        pass

    def try_map(self):
        # Add code to try the map in experimental mode
        pass

    def no_solution(self):
        # Add code for "No Solution" button in normal mode
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MapEditor(root)
    root.mainloop()
