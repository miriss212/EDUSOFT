import tkinter as tk
from PIL import Image, ImageTk

class WindowEditor:
    # trieda pre vykreslovanie vsetkeho v okne

    BORDER_WIDTH = 3

    WINDOW_SIZE = (505, 500)
    BUTTONS_AREA_SIZE = (WINDOW_SIZE[0], 50 - BORDER_WIDTH)
    CANVAS_SIZE = (WINDOW_SIZE[0] - 2 * BORDER_WIDTH, WINDOW_SIZE[1] - BUTTONS_AREA_SIZE[1] - BORDER_WIDTH)

    FONT = ('Comic Sans MS', 12)
    CELL_SIZE = 35
    COMMAND_SIZE = 45

    def __init__(self) -> None:
        self._set_master_window()    
        self._set_canvas()
        self._set_buttons_area()
        self._load_images()

        #self.master.mainloop()

    def _set_master_window(self) -> None:
        self.master = tk.Tk()
        self.master.geometry(f"{WindowEditor.WINDOW_SIZE[0]}x{WindowEditor.WINDOW_SIZE[1]}")
        self.master.resizable(False, False)  # Toto zakáže zmenu veľkosti okna
        self.master.title("Edusoft – Ponorka")

    def _set_canvas(self) -> None:
        self.canvas = tk.Canvas(self.master, height = WindowEditor.CANVAS_SIZE[1], width = WindowEditor.CANVAS_SIZE[0], bg = "white", bd = 0, cursor = "hand2")
        self.canvas.place(x = 0, y = 0)
        self._set_background_image()

    def _set_buttons_area(self) -> None:
        self.buttons_area = tk.Frame(self.master, height = WindowEditor.BUTTONS_AREA_SIZE[1], width = WindowEditor.BUTTONS_AREA_SIZE[0], bd = 0)
        self.buttons_area.place(x = 0, y = WindowEditor.CANVAS_SIZE[1] + WindowEditor.BORDER_WIDTH)

    def _set_background_image(self) -> None:
        background_image = Image.open("images/background_texture.png").resize((WindowEditor.WINDOW_SIZE[0], WindowEditor.WINDOW_SIZE[1]), Image.LANCZOS)
        self.background_image_id = ImageTk.PhotoImage(background_image)
        self.canvas.create_image(0, 0, image = self.background_image_id, anchor = "nw")

    def set_execute_commands_button(self, execute_commands_function: callable) -> None:
        self.execute_commands_button = tk.Button(self.buttons_area, text = "Spustiť príkazy!", font = WindowEditor.FONT, command = execute_commands_function)
        self.execute_commands_button.grid(row=0, column=2)
        
    def set_restart_game_button(self, restart_game_function: callable) -> None:
        self.restart_game_button = tk.Button(self.buttons_area, text = "Reštart", font = WindowEditor.FONT, command = restart_game_function)
        self.restart_game_button.grid(row=0, column=3)

    def set_new_game_button(self, new_game_function: callable) -> None:
        self.new_game_button = tk.Button(self.buttons_area, text = "Nová hra...", font = WindowEditor.FONT, command = new_game_function)
        self.new_game_button.grid(row=0, column=4)

    def set_sonar_slider(self, from_: int, to: int, sonar_slider_function: callable) -> None:
        self.sonar_slider = tk.Scale(self.buttons_area, from_ = from_, to = to, orient = "horizontal", font = WindowEditor.FONT, command = sonar_slider_function)
        label = tk.Label(self.buttons_area, text = "Hĺbka sonaru:", font = WindowEditor.FONT)
        label.grid(row=0, column=0)
        self.sonar_slider.grid(row=0, column=1)

    def redraw_canvas(self, sonar_view: list[list[str]], submarine_position: tuple, submarine_oxygen: int, command_list: list, actual_command_index: int, submarine_direction: str) -> None:
        self.canvas.delete("all")
        self._set_background_image()

        sonar_view_rows_count = len(sonar_view)
        sonar_view_columns_count = len(sonar_view[0])

        self._draw_grid(sonar_view_rows_count, sonar_view_columns_count)
        self._draw_icons(sonar_view, submarine_position, submarine_direction)
        self._draw_commands(command_list, actual_command_index)
        self._draw_oxygen(submarine_oxygen)

    # (pocet riadkov, pocet stlpcov)
    def _draw_grid(self, rows, columns):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        cell_width = WindowEditor.CELL_SIZE
        cell_height = WindowEditor.CELL_SIZE

        # velkost gridu
        total_width = columns * cell_width
        total_height = rows * cell_height

        # vycentrovat grid na stred
        start_x = (canvas_width - total_width) // 2
        start_y = (canvas_height - total_height) // 2

        self._create_rounded_rectangle(cell_width*(columns+1), cell_height*(rows+1), 20, fill='DodgerBlue3', outline='black', border_width=2)

        # vertikalne ciarky
        for i in range(0, columns + 1):
            x = start_x + i * cell_width
            self.canvas.create_line(x, start_y, x, start_y + total_height, fill="black")

        # horizontalne ciarky
        for j in range(0, rows + 1):
            y = start_y + j * cell_height
            self.canvas.create_line(start_x, y, start_x + total_width, y, fill="black")

    def _create_rounded_rectangle(self, width, height, radius, **kwargs):
        border_width = kwargs.pop('border_width', 1)

        # Calculate the starting point to center the rectangle
        start_x = (self.canvas.winfo_reqwidth() - width) // 2 
        start_y = (self.canvas.winfo_reqheight() - height) // 2 

        points = [
            start_x + radius, start_y,
            start_x + width - radius, start_y,
            start_x + width, start_y + radius,
            start_x + width, start_y + height - radius,
            start_x + width - radius, start_y + height,
            start_x + radius, start_y + height,
            start_x, start_y + height - radius,
            start_x, start_y + radius,
        ]

        self.canvas.create_polygon(points, outline=kwargs.get('outline', 'lightblue'), fill=kwargs.get('fill', ''), width=border_width, tags="rounded_rect")

    def _draw_icons(self, sonar_view: list[list[str]], submarine_position: tuple, submarine_direction: str) -> None:
        
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        
        column_count = len(sonar_view[0])
        row_count = len(sonar_view)

        total_width = column_count * WindowEditor.CELL_SIZE
        total_height = row_count * WindowEditor.CELL_SIZE

        start_x = (canvas_width - total_width) // 2
        start_y = (canvas_height - total_height) // 2

        sonar_value = int(self.sonar_slider.get())
        submarine_level, submarine_row, submarine_column = submarine_position
        if sonar_value == submarine_level:
            self._update_submarine_image(submarine_position, submarine_direction, sonar_view)

        #self.update_oxygen_label(game_manager.game.submarine_oxygen) # TODO

        # Add an image to the cell where "B" is located in the current level
        for row, columns in enumerate(sonar_view):
            for column, cell in enumerate(columns):
                x = start_x + column * WindowEditor.CELL_SIZE
                y = start_y + row * WindowEditor.CELL_SIZE

                if cell == "B":
                    img_bubble = Image.open("images/bubble.png")
                    img_bubble = img_bubble.resize((WindowEditor.CELL_SIZE, WindowEditor.CELL_SIZE), Image.LANCZOS)
                    img_bubble_id = ImageTk.PhotoImage(img_bubble)
                    self.bubble_img_ids.append(img_bubble_id)
                    self.canvas.create_image(x + WindowEditor.CELL_SIZE // 2, y + WindowEditor.CELL_SIZE // 2, anchor = tk.CENTER, image = img_bubble_id)
                
                if cell == "P":
                    img_coin = Image.open("images/coin.png")
                    img_coin = img_coin.resize((WindowEditor.CELL_SIZE + 15, WindowEditor.CELL_SIZE + 15), Image.LANCZOS)
                    self.img_coin_id = ImageTk.PhotoImage(img_coin)
                    self.canvas.create_image(x + WindowEditor.CELL_SIZE // 2, y + WindowEditor.CELL_SIZE // 2, anchor = tk.CENTER, image = self.img_coin_id)

                if cell == "K":
                    img_rock = Image.open("images/rock.png")
                    img_rock = img_rock.resize((WindowEditor.CELL_SIZE, WindowEditor.CELL_SIZE), Image.LANCZOS)
                    img_rock_id = ImageTk.PhotoImage(img_rock)
                    self.rock_img_ids.append(img_rock_id)
                    self.canvas.create_image(x + WindowEditor.CELL_SIZE // 2, y + WindowEditor.CELL_SIZE // 2, anchor = tk.CENTER, image = img_rock_id)

    def _update_submarine_image(self, submarine_position: tuple, direction: str, sonar_view: list[list[str]]) -> None:
        if (
            self.submarine_image_left is not None
            and self.submarine_image_right is not None
            and self.submarine_image_up is not None
            and self.submarine_image_down is not None
        ):
            submarine_level, submarine_row, submarine_column = submarine_position
            canvas_width = self.canvas.winfo_reqwidth()
            canvas_height = self.canvas.winfo_reqheight()
            
            column_count = len(sonar_view[0])
            row_count = len(sonar_view)

            total_width = column_count * WindowEditor.CELL_SIZE
            total_height = row_count * WindowEditor.CELL_SIZE

            start_x = (canvas_width - total_width) // 2
            start_y = (canvas_height - total_height) // 2

            x = (submarine_column * WindowEditor.CELL_SIZE) + (WindowEditor.CELL_SIZE // 2) + start_x
            y = (submarine_row * WindowEditor.CELL_SIZE) + (WindowEditor.CELL_SIZE // 2) + start_y

            submarine_image = None
            if direction == "left":
                submarine_image = self.submarine_image_left
            elif direction == "right":
                submarine_image = self.submarine_image_right
            elif direction == "up":
                submarine_image = self.submarine_image_up
            elif direction == "down":
                submarine_image = self.submarine_image_down

            if self.submarine_image_id:
                self.canvas.delete(self.submarine_image_id)

            self.submarine_image_id = self.canvas.create_image(x, y, anchor=tk.CENTER, image=submarine_image)

    def _load_images(self):
        self.submarine_image_id = None

        self.rock_img_ids = []
        self.bubble_img_ids = []
        self.coin_img_ids = []

        img_left = Image.open("images/left_sub.png")
        img_left = img_left.resize((WindowEditor.CELL_SIZE, WindowEditor.CELL_SIZE), Image.LANCZOS)
        self.submarine_image_left = ImageTk.PhotoImage(img_left)

        img_right = Image.open("images/right_sub.png")  # Replace with the actual path
        img_right = img_right.resize((WindowEditor.CELL_SIZE, WindowEditor.CELL_SIZE), Image.LANCZOS)
        self.submarine_image_right = ImageTk.PhotoImage(img_right)

        img_up = Image.open("images/up_sub.png")
        img_up = img_up.resize((WindowEditor.CELL_SIZE, WindowEditor.CELL_SIZE), Image.LANCZOS)
        self.submarine_image_up = ImageTk.PhotoImage(img_up)

        img_down = Image.open("images/down_sub.png")  # Replace with the actual path
        img_down = img_down.resize((WindowEditor.CELL_SIZE, WindowEditor.CELL_SIZE), Image.LANCZOS)
        self.submarine_image_down = ImageTk.PhotoImage(img_down)

    def _draw_commands(self, command_list: list, actual_command_index: int) -> None:
        x = 25
        y = 25

        for rectangle in range(10):
            self.canvas.create_rectangle(x, y, x + WindowEditor.COMMAND_SIZE, y + WindowEditor.COMMAND_SIZE, fill="white", outline="black")
            x += WindowEditor.COMMAND_SIZE

        x = 25
        y = 25

        for index, command in enumerate(command_list):
            if actual_command_index is not None and index == actual_command_index:
                self.canvas.create_rectangle(x, y, x + WindowEditor.COMMAND_SIZE, y + WindowEditor.COMMAND_SIZE, fill="green", outline="black")

            self.canvas.create_image(x + WindowEditor.COMMAND_SIZE // 2, y + WindowEditor.COMMAND_SIZE // 2, anchor=tk.CENTER, image = command.command_img)
                
            x += WindowEditor.COMMAND_SIZE

    def _draw_oxygen(self, submarine_oxygen: int) -> None:
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        self.canvas.create_rectangle(canvas_width // 2 - 75, canvas_height - 35, canvas_width // 2 + 75, canvas_height - 15, fill="white", outline="black")
        self.canvas.create_text(canvas_width // 2, canvas_height - 25, text = f"Zostavajúci vzduch: {submarine_oxygen}", anchor=tk.CENTER, font = WindowEditor.FONT)