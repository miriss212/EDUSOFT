import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.font as tkFont
import os
import backend

class MapEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Jedným ťahom")

        self.mode = "normal"  # Initial mode is normal
        
        # Open a JPEG image and convert it to PhotoImage
        self.background_image = self.load_and_resize_image("room.png", 44*12, 44*10)

        self.canvas = tk.Canvas(root, width=44*12, height=44*10)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)  # Set the image as the background
        self.canvas.grid(row=1, column=0, columnspan=4)

        self.game_area_manager = backend.GameAreaManager(self.canvas)
        self.canvas.bind("<KeyPress>", self.on_key_press)
        self.canvas.focus_set() 

        custom_font = tkFont.Font(family="Lucida Sans Unicode", size=16, weight="bold", slant="italic")
        universal_font = tkFont.Font(family="Lucida Sans Unicode", size=14, weight="normal", slant="italic")
        self.mode_label = tk.Label(root, text="Mode: " + self.mode, bg="sandybrown", font=custom_font)
        self.mode_label.grid(row=0, column=0, columnspan=2)
        self.universal_label = tk.Label(root, text="", bg="sandybrown", font=universal_font)
        self.universal_label.grid(row=2, column=0, columnspan=4)
        self.universal_label.config(text="Vyber mapu ktorú chceš hrať pomocou ikonky!")

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.grid(row=3, column=0, columnspan=5)

        self.switch_button = tk.Button(self.buttons_frame, text="Switch Mode", command=self.toggle_mode, bg='sandybrown')
        self.switch_button.grid(row=0, column=0, padx=5, pady=5)

        img1 = Image.open("save.png")
        img1 = img1.resize((30, 30), Image.NEAREST)
        photo1 = ImageTk.PhotoImage(img1)

        img_reset= Image.open("reset.png")
        img_reset = img_reset.resize((30, 30), Image.NEAREST)
        photo_reset = ImageTk.PhotoImage(img_reset)

        img_open = Image.open("open.png")
        img_open =  img_open.resize((30, 30), Image.NEAREST)
        photo_open = ImageTk.PhotoImage(img_open)

        img_find = Image.open("solution.png")
        img_find  =  img_find .resize((30, 30), Image.NEAREST)
        photo_find = ImageTk.PhotoImage(img_find)

        img_no_sol = Image.open("no_sol.png")
        img_no_sol =  img_no_sol.resize((30, 30), Image.NEAREST)
        photo_no_sol = ImageTk.PhotoImage(img_no_sol)

        self.save_button = tk.Button(self.buttons_frame, text="Save Map",image=photo1, command=self.save_map)
        self.save_button.image = photo1
        self.open_button = tk.Button(self.buttons_frame, text="Open Map", command=self.open_map, image=photo_open)
        self.open_button.image = photo_open
        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_map, image=photo_reset)
        self.reset_button.image = photo_reset
        self.try_button = tk.Button(self.buttons_frame, text="Try Map", command=self.try_map, image=photo_find)
        self.try_button.image = photo_find
        self.no_solution_button = tk.Button(self.buttons_frame, text="No Solution", command=self.no_solution, image = photo_no_sol)
        self.no_solution_button.image = photo_no_sol
        self.save_button.grid(row=0, column=1, padx=5, pady=5)
        self.open_button.grid(row=0, column=2, padx=5, pady=5)
        self.reset_button.grid(row=0, column=3, padx=5, pady=5)
        self.try_button.grid(row=0, column=4, padx=5, pady=5)
        self.no_solution_button.grid(row=0, column=5, padx=5, pady=5)

        self.create_size_sliders()

        self.set_button_states()  # Set initial button states

    def on_key_press(self, event):
        if self.game_area_manager.on_key_press(event) == True:
            self.universal_label.config(text="Výborne, vyhral si! Vyber ďalšiu mapu...")

    def load_and_resize_image(self, path, width, height):
        original_image = Image.open(path)
        resized_image = original_image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def toggle_mode(self):
        self.mode = "experimental" if self.mode == "normal" else "normal"
        self.set_button_states()
        self.mode_label.config(text="Mode: " + self.mode)

        if self.mode == "normal":
            self.universal_label.config(text="Snaž sa! Môžeš použiť nápovedu pomocou ikonky...")
        if self.mode == "experimental":
            self.universal_label.config(text="Ľavým klikom pridaj krabicu, pravým hráča...")

    def set_button_states(self):
        if self.mode == "normal":
            self.save_button.grid_forget()
            self.open_button.grid(row=0, column=1)
            self.reset_button.grid(row=0, column=2)
            self.try_button.grid(row=0, column=3)
            self.size_x_label.grid_forget()
            self.size_y_label.grid_forget()
            self.size_x_slider.grid_forget()
            self.size_y_slider.grid_forget()
            self.submit_resize_button.grid_forget()
            self.no_solution_button.grid(row=0, column=4, padx=5, pady=5)
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.canvas.bind("<KeyPress>", self.on_key_press)
        else:
            self.save_button.grid(row=0, column=1)
            self.open_button.grid_forget()
            self.reset_button.grid(row=0, column=2)
            self.try_button.grid(row=0, column=3)
            self.size_x_label.grid(row=1, column=1, padx=5, pady=5)
            self.size_x_slider.grid(row=1, column=2, padx=5, pady=5)
            self.size_y_label.grid(row=2, column=1, padx=5, pady=5)
            self.size_y_slider.grid(row=2, column=2, padx=5, pady=5)
            self.submit_resize_button.grid(row=1, column=3, padx=5, pady=5)
            self.no_solution_button.grid_forget()
            self.canvas.bind("<Button-1>", self.manage_left_click)
            self.canvas.bind("<Button-3>", self.manage_right_click)
            self.canvas.unbind("<KeyPress>")
            

    def manage_left_click(self, event):
        self.game_area_manager.add_object_to_game_area(event)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.game_area_manager.game_area_renderer.render_game_area()

    def manage_right_click(self, event):
        self.game_area_manager.add_player_to_game_area(event)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.game_area_manager.game_area_renderer.render_game_area()

    def create_size_sliders(self):
        self.size_x_label = tk.Label(self.buttons_frame, text="Set X Size:", bg="sandybrown")
        self.size_x_slider = tk.Scale(self.buttons_frame, from_= 2, to= 10, orient="horizontal", length=200, bg='#ffc299', highlightbackground='#ff6600')
        self.size_x_slider.set(5)
        self.size_x_label.grid(row=1, column=1, padx=5, pady=5)
        self.size_x_slider.grid(row=1, column=2, padx=5, pady=5)

        self.size_y_label = tk.Label(self.buttons_frame, text="Set Y Size:", bg="sandybrown")
        self.size_y_slider = tk.Scale(self.buttons_frame, from_= 2, to= 8, orient="horizontal", length=200, bg='#ffc299', highlightbackground='#ff6600')
        self.size_y_slider.set(5)
        self.size_y_label.grid(row=2, column=1, padx=5, pady=5)
        self.size_y_slider.grid(row=2, column=2, padx=5, pady=5)

        img2 = Image.open("submit.png")
        img2 = img2.resize((30, 30), Image.NEAREST)
        photo2 = ImageTk.PhotoImage(img2)
        self.submit_resize_button = tk.Button(self.buttons_frame, text="Submit Resize", command=self.submit_resize, image = photo2)
        self.submit_resize_button.image = photo2

    def submit_resize(self):
        new_size_x = self.size_x_slider.get()
        new_size_y = self.size_y_slider.get()
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.game_area_manager.create_empty_game_area(new_size_x, new_size_y)
        self.game_area_manager.game_area_renderer.render_game_area()

    def resize_canvas(self, width, height):
        self.canvas.config(width=width, height=height)
        self.background_image = self.load_and_resize_image("sand.jpg", width, height)
        self.canvas.itemconfig(1, image=self.background_image)
    

    def save_map(self):
        # Define the file type for .txt files
        filetypes = [
            ("Text Files", "*.txt")
        ]

        # Configure options for the dialog
        options = {
            'defaultextension': '.txt',  # Default file extension
            'filetypes': filetypes,  # List of file types
            'initialdir': 'mapky'
        }

        # Open a file dialog to get the save file path
        self.file_path = filedialog.asksaveasfilename(**options)
        self.game_area_manager.save_game_area_to_file(self.file_path)
        print(self.file_path)

    def open_map(self):
        # Add code to open a saved map in normal mode
        # file_path = filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)))
        # file_path = filedialog.askopenfilename(initialdir=".", title="Select a Text File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
 
        # Configure options for the dialog
        options = {
            'defaultextension': '.txt',  # Default file extension
            'filetypes': [("Text Files", "*.txt")],  # List of file types
            'initialdir': 'mapky'
        }
 
        # Open a file dialog with the configured options
        self.file_path = filedialog.askopenfilename(**options)
        if self.file_path: # bolo by dobre dat do priecinka mapky
        # Do something with the selected file (e.g., print its path)
            print("Selected file:", self.file_path)
            self.game_area_manager.create_game_area_from_file(self.file_path)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
            self.game_area_manager.game_area_renderer.render_game_area()
            self.universal_label.config(text="Snaž sa! Môžeš použiť nápovedu pomocou ikonky...")

    def reset_map(self):

        if self.mode == "experimental":  
            self.game_area_manager.create_empty_game_area(self.size_x_slider.get(),self.size_y_slider.get())
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
            self.game_area_manager.game_area_renderer.render_game_area()
        else :
            print(self.file_path)
            self.game_area_manager.create_game_area_from_file(self.file_path)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
            self.game_area_manager.game_area_renderer.render_game_area()
            self.universal_label.config(text="Snaž sa! Môžeš použiť nápovedu pomocou ikonky...")
        

    def try_map(self):
        # Add code to try the map in experimental mode
        solver = backend.HamiltonianPathSolver(self.game_area_manager.game_area)
        hamiltonian_path = solver.get_hamiltonian_path()
        if hamiltonian_path == []:
            self.universal_label.config(text="Cesta už neexistuje... Daj reset!")
        else:
            self.game_area_manager.game_area_renderer.show_hamiltonian_path(hamiltonian_path)

    def no_solution(self):
        # Add code for "No Solution" button in normal mode
        solver = backend.HamiltonianPathSolver(self.game_area_manager.game_area)
        hamiltonian_path = solver.get_hamiltonian_path()
        if hamiltonian_path == []:
            self.universal_label.config(text="Správne! Táto mapa nemá riešenie, vyber ďalšiu mapu!")
        else:
            self.universal_label.config(text="Táto mapa má riešenie, snaž sa ďalej!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapEditor(root)
    root.mainloop()
    
