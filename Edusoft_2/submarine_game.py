import tkinter as tk
from PIL import Image, ImageTk
class Game:

    BUBBLE_VALUE: int = 5

    def __init__(self, map_file_path: str) -> None:
        self.map_file_path: str = map_file_path
        
        self.game_field: list[list[list[str]]] = None
        self.submarine_position: tuple[int, int, int] = None # [level, row, column]
        self.submarine_oxygen: int = None
        self._generate_game_field()

    def restart_game(self) -> None:
        self._generate_game_field()

    def get_sonar_view(self, level: int) -> list[list[str]]:
        if 0 <= level < len(self.game_field):
            return self.game_field[level]
        
    def check_win(self) -> bool:
        return self.game_field[self.submarine_position[0]][self.submarine_position[1]][self.submarine_position[2]] == "P"
    
    def check_lose(self) -> bool:
        return self.submarine_oxygen <= 0
    
    def go_shallower(self) -> bool:
        return self._move_to(self.submarine_position[0] - 1, self.submarine_position[1], self.submarine_position[2])

    def go_deeper(self) -> bool:
        return self._move_to(self.submarine_position[0] + 1, self.submarine_position[1], self.submarine_position[2])

    def go_forward(self) -> bool:
        return self._move_to(self.submarine_position[0], self.submarine_position[1] - 1, self.submarine_position[2])

    def go_back(self) -> bool:
        return self._move_to(self.submarine_position[0], self.submarine_position[1] + 1, self.submarine_position[2])

    def go_left(self) -> bool:
        return self._move_to(self.submarine_position[0], self.submarine_position[1], self.submarine_position[2] - 1)

    def go_right(self) -> bool:
        return self._move_to(self.submarine_position[0], self.submarine_position[1], self.submarine_position[2] + 1)
    
    def _generate_game_field(self) -> None:
        self.game_field = []

        with open(self.map_file_path, 'r') as map_file:
            map_file_content = map_file.read()

        for level_content in map_file_content.split('\n\n')[:-1]:
            level = [list(field) for field in level_content.split('\n')]
            self.game_field.append(level)

        submarine_data = map_file_content.split('\n\n')[-1].split(",")
        self.submarine_position = (int(submarine_data[0]), int(submarine_data[1]), int(submarine_data[2]))
        self.submarine_oxygen = int(submarine_data[3])

    # vrati True ak sa podarilo pohnut, inak False ak sa nepodarilo
    def _move_to(self, level: int, row: int, column: int) -> bool:
        if not 0 <= level < len(self.game_field):
            return False
        if not 0 <= row < len(self.game_field[level]):
            return False
        if not 0 <= column < len(self.game_field[level][row]):
            return False
        if self.game_field[level][row][column] == "K":
            return False
        
        # doplnenie oxygenu
        if self.game_field[level][row][column] == "B":
            self.submarine_oxygen += Game.BUBBLE_VALUE

        self.submarine_position = (level, row, column)
        self.submarine_oxygen -= 1
        return True

class WindowEditor:
    def __init__(self, master):
        self.master = master
        self.canvas = None
        self.oxygen_label = None
        self.depth_slider = None
        self.cell_size = 30
        self.arrow_up_image = None
        self.arrow_down_image = None
        self.arrow_left_image = None
        self.arrow_right_image = None
        self.arrow_buttons = None

    def create_canvas(self, width, height):
        self.canvas = tk.Canvas(self.master, width=width, height=height, bg="white")
        self.canvas.pack()

    def draw_grid(self, rows, columns):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        # Calculate fixed cell size
        cell_width = self.cell_size
        cell_height = self.cell_size

        # Calculate the total size of the grid
        total_width = columns * cell_width
        total_height = rows * cell_height

        # Calculate the starting position to center the grid
        start_x = (canvas_width - total_width) // 2
        start_y = (canvas_height - total_height) // 2

        # Draw vertical lines
        for i in range(0, columns + 1):
            x = start_x + i * cell_width
            self.canvas.create_line(x, start_y, x, start_y + total_height, fill="black")

        # Draw horizontal lines
        for j in range(0, rows + 1):
            y = start_y + j * cell_height
            self.canvas.create_line(start_x, y, start_x + total_width, y, fill="black")

        # Add oxygen label
        self.oxygen_label = tk.StringVar()
        self.oxygen_label.set("Oxygen: N/A")
        label = tk.Label(self.master, textvariable=self.oxygen_label)
        label.pack()

        # Add depth slider
        self.depth_slider = tk.Scale(self.master, from_=1, to=rows, orient=tk.HORIZONTAL, label="Depth",
                                     length=300, sliderlength=20, command=self.update_depth)
        self.depth_slider.pack()

        # Add Confirm Depth button
        confirm_button = tk.Button(self.master, text="Confirm Depth", command=self.confirm_depth)
        confirm_button.pack()

    def update_oxygen_label(self, oxygen_level):
        self.oxygen_label.set(f"Oxygen: {oxygen_level}%")

    def update_depth(self, depth):
        print(f"Submarine depth set to: {depth}")

    def confirm_depth(self):
        selected_depth = self.depth_slider.get()
        print(f"Confirmed depth: {selected_depth}")

    def add_button(self, text, command):
        button = tk.Button(self.master, text=text, command=command)
        button.pack()


    def add_arrow_buttons(self):
        img1 = Image.open("c:\\Users\\cidom\\OneDrive\\Dokumenty\\mAIN2\\EDUSOFT-1\\Edusoft_2\\arrow_up.png")
        img1 = img1.resize((30, 30), Image.NEAREST)
        self.arrow_up_image = ImageTk.PhotoImage(img1)

        img2 = Image.open("c:\\Users\\cidom\\OneDrive\\Dokumenty\\mAIN2\\EDUSOFT-1\\Edusoft_2\\arrow_right.png")
        img2 = img2.resize((30, 30), Image.NEAREST)
        self.arrow_right_image = ImageTk.PhotoImage(img2)

        img3 = Image.open("c:\\Users\\cidom\\OneDrive\\Dokumenty\\mAIN2\\EDUSOFT-1\\Edusoft_2\\arrow_left.png")
        img3 = img3.resize((30, 30), Image.NEAREST)
        self.arrow_left_image = ImageTk.PhotoImage(img3)

        img4 = Image.open("c:\\Users\\cidom\\OneDrive\\Dokumenty\\mAIN2\\EDUSOFT-1\\Edusoft_2\\arrow_down.png")
        img4 = img4.resize((30, 30), Image.NEAREST)
        self.arrow_down_image = ImageTk.PhotoImage(img4)

        button_frame = tk.Frame(self.master)
        button_frame.pack()

        arrow_up_button = tk.Button(button_frame, image=self.arrow_up_image, command=self.move_up, compound='top', padx=10, pady=10)
        arrow_down_button = tk.Button(button_frame, image=self.arrow_down_image, command=self.move_down, compound='bottom', padx=10, pady=10)
        arrow_left_button = tk.Button(button_frame, image=self.arrow_left_image, command=self.move_left, compound='left', padx=50, pady=50)
        arrow_right_button = tk.Button(button_frame, image=self.arrow_right_image, command=self.move_right, compound='right', padx=5, pady=5)

        arrow_up_button.grid(row=0, column=1, padx=5, pady=5)
        arrow_down_button.grid(row=2, column=1, padx=5, pady=5)
        arrow_left_button.grid(row=1, column=0, padx=5, pady=5)
        arrow_right_button.grid(row=1, column=2, padx=5, pady=5)

        self.master.bind("<Up>", lambda event: self.move_up())
        self.master.bind("<Down>", lambda event: self.move_down())
        self.master.bind("<Left>", lambda event: self.move_left())
        self.master.bind("<Right>", lambda event: self.move_right())

    def move_up(self):
        if map_editor is not None:
            game_manager.game.go_forward()
            self.update_game_display(game_manager)

    def move_down(self):
        if map_editor is not None:
            game_manager.game.go_back()
            self.update_game_display(game_manager)
            

    def move_left(self):
        if map_editor is not None:
            game_manager.game.go_left()
            self.update_game_display(game_manager)

    def move_right(self):
        if map_editor is not None:
            game_manager.game.go_right()
            self.update_game_display(game_manager)

    

    def update_game_display(self, game_manager):
        # Clear the canvas
        self.canvas.delete("all")

        # Redraw the grid
        self.draw_grid(rows=3, columns=4)
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        total_width = 4 * self.cell_size
        total_height = 3 * self.cell_size

        start_x = (canvas_width - total_width) // 2
        start_y = (canvas_height - total_height) // 2

        # Draw the submarine
        submarine_level, submarine_row, submarine_column = game_manager.game.submarine_position
        print(submarine_column)
        cell_size = self.cell_size

        # Calculate the coordinates for the submarine
        
        x = start_x + submarine_column * cell_size
        y = start_y + submarine_row * cell_size

        # Draw a rectangle representing the submarine
        submarine_rect = self.canvas.create_rectangle(
            x, y, x + cell_size, y + cell_size, fill="blue", outline="black"
        )

        # TODO: Add code to draw other game elements as needed

        # Update the oxygen label
        self.update_oxygen_label(game_manager.game.submarine_oxygen)

        # Update the depth slider (assuming the depth is the level of the submarine)
        self.depth_slider.set(submarine_level)

        # Update the canvas
        self.canvas.update()

class Command:
    # commandy ktore hrac pridava do postupnosti a cela postupnost sa potom skusti cez GameManager.execute_commands()
    
    def __init__(self) -> None:
        self.game: Game = None
        self.map_editor: WindowEditor = None
        # referencie na objekty sa nastavuju neskor objektom ktory pridava commandy do postupnosti

    def execute(self) -> None:
        raise NotImplementedError("This is abstract method!")
        # skonci ak ponorka narazi alebo ak nastane vyhra/prehra
    
class GoShallowerCommand(Command):
    
    def execute(self) -> None:
        while self.game.go_shallower():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit novu poziciu ponorky cez self.map_editor (+ prepnut sonar na level kde sa nachadza ponorka)

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoDeeperCommand(Command):
    
    def execute(self) -> None:
        while self.game.go_deeper():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit novu poziciu ponorky cez self.map_editor (+ prepnut sonar na level kde sa nachadza ponorka)

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoForwardCommand(Command):
    
    def execute(self) -> None:
        while self.game.go_forward():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit novu poziciu ponorky cez self.map_editor (+ prepnut sonar na level kde sa nachadza ponorka)

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoBackCommand(Command):
    
    def execute(self) -> None:
        while self.game.go_back():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit novu poziciu ponorky cez self.map_editor (+ prepnut sonar na level kde sa nachadza ponorka)

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoLeftCommand(Command):

    def execute(self) -> None:
        while self.game.go_left():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit novu poziciu ponorky cez self.map_editor (+ prepnut sonar na level kde sa nachadza ponorka)

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoRightCommand(Command):

    def execute(self) -> None:
        while self.game.go_right():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit novu poziciu ponorky cez self.map_editor (+ prepnut sonar na level kde sa nachadza ponorka)

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break
    
class GameManager:
    # TODO: trieda pre riadenie celej hry (aplikacie)

    def __init__(self, map_editor: WindowEditor) -> None:
        self.map_editor: WindowEditor = map_editor
        self.game: Game = None

        self.commands: list[Command] = []
        # TODO: vykreslit okno s prazdnym canvasom lebo self.game == None (hra sa vybere zo suboru)

    def add_command(self, command: Command) -> None:

        # tu sa nastavia referencie na objekty
        command.game = self.game
        command.map_editor = self.map_editor

        self.commands.append(command)
        # TODO: nanovo vykreslit commandy

    def remove_last_command(self) -> None:
        if len(self.commands) > 0:
            self.commands.pop()
        # TODO: nanovo vykreslit commandy

    def execute_commands(self) -> None:
        for command in self.commands:
            # TODO: oznac vykonavany command cez self.map_editor
            command.execute()
            self.map_editor.update_game_display(game_manager) 
            if command.game.check_lose():
                # TODO: osetrit prehru
                return
            if command.game.check_win():
                # TODO: osetrit vyhru
                return
        # TODO: ponorka ostala na polceste (restart hry?)

    # nova hra ked si hrac vybere nejaku mapu
    def new_game(self, map_file_path: str) -> None:
        self.game = Game(map_file_path)

        self.commands = []
        # TODO: nanovo vykreslit hru

    def restart_game(self) -> None:
        if self.game is not None:
            self.game.restart_game()

        self.commands = []
        # TODO: nanovo vykreslit hru

#test
root = tk.Tk()
root.title("Submarine Game")

map_editor = WindowEditor(root)
map_editor.create_canvas(500, 400)
map_editor.draw_grid(rows=3, columns=4) 
map_editor.add_arrow_buttons()
# Simulate updating the oxygen label
map_editor.update_oxygen_label(oxygen_level=80)

game_manager = GameManager(map_editor)
# Create a new game before executing any commands
game_manager.new_game("Edusoft_2/test_map.txt")
map_editor.update_game_display(game_manager)

root.mainloop()