import copy
import os
import tkinter as tk
from PIL import Image, ImageTk

class Field: # policko

    def __init__(self, has_object: bool, x_position: int, y_position: int) -> None:
        self.x_position = x_position
        self.y_position = y_position
        self.is_visited = False
        self.has_object = has_object # True / False

class GameArea: # herna plocha (stvorcova siet policok)

    def __init__(self, fields: list, x_size: int, y_size: int, player_position: tuple) -> None:
        self.fields = fields
        self.x_size = x_size
        self.y_size = y_size
        self.player_position = player_position
        # self.get_field_by_position(player_position[0], player_position[1]).is_visited = True

    def is_valid_move(self, to_x, to_y) -> bool:
        to_field = self.get_field_by_position(to_x, to_y)
        if to_field is None: # mimo hracej plochy
            return False
        elif (to_field.has_object or to_field.is_visited): # na policku je objekt alebo je uz navstiveny
            return False
        else:
            return True

    def get_field_by_position(self, x_position: int, y_position: int) -> Field:
        for field in self.fields:
            if (field.x_position == x_position and field.y_position == y_position):
                return field
        return None
    
    def check_win(self) -> bool:
        player_field = self.get_field_by_position(self.player_position[0], self.player_position[1])
        for field in self.fields:
            if not field.is_visited and field != player_field: # ak neni navstivene a zaroven na nom neni hrac
                return False
        return True
    
    def move_player(self, direction: str):
        valid_moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        new_player_position = (self.player_position[0] + valid_moves[direction][0], self.player_position[1] + valid_moves[direction][1])
        if self.is_valid_move(new_player_position[0], new_player_position[1]):
            self.get_field_by_position(self.player_position[0], self.player_position[1]).is_visited = True # oznac policko ako navstivene
            self.player_position = new_player_position
            #self.game_area_renderer.update_game_area() 

class HamiltonianPathSolver:

    def __init__(self, game_area: GameArea) -> None:
        self.game_area = copy.deepcopy(game_area) # rekurzivne kopiruje do hlbky vsetky elementy

    def get_hamiltonian_path(self) -> list: # https://stackoverflow.com/questions/47982604/hamiltonian-path-using-python
        # pracujeme len so suradnicami
        fields_size = self.get_game_area_size()
        to_visit = [None, self.game_area.player_position] # startujeme od pozicie hraca
        hamiltonian_path = []
        while (to_visit):
            field_coordinates = to_visit.pop()
            if field_coordinates:
                hamiltonian_path.append(field_coordinates)
                if len(hamiltonian_path) == fields_size:
                    break
                for neighbour in set(self.get_valid_neighbours(field_coordinates)) - set(hamiltonian_path):
                    to_visit.append(None)
                    to_visit.append(neighbour)
            else:
                hamiltonian_path.pop()
        return hamiltonian_path

    def get_valid_neighbours(self, field_coordinates: tuple) -> list: # vracia suradnice policok
        valid_neighbours = []
        valid_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # hore, dole, doprava, dolava
        for d_x, d_y in valid_moves:
            neighbour_coordinates = (field_coordinates[0] + d_x, field_coordinates[1] + d_y)
            if self.game_area.is_valid_move(neighbour_coordinates[0], neighbour_coordinates[1]): # ak je sused validny
                valid_neighbours.append(neighbour_coordinates) # pridavame suradnice policka
        return valid_neighbours

    def get_field_coordinates(self, field: Field) -> tuple: # (x, y)
        return (field.x_position, field.y_position)

    def get_game_area_size(self) -> int:
        game_area_size = 0 # validne policka, pozor policko na ktorom je hrac navstivene este nie je!
        for field in self.game_area.fields:
            if self.game_area.is_valid_move(field.x_position, field.y_position):
                game_area_size += 1
        return game_area_size

class GameAreaManager:

    def __init__(self, canvas) -> None:
        self.game_area = None
        self.game_area_renderer = None
        self.canvas = canvas
        
    def create_empty_game_area(self, x_size: int, y_size: int) -> None:

        fields = []
        player_position = (0 ,0) # (x, y)
        for y in range(y_size):
            for x in range(x_size):
                fields.append(Field(False, x, y))
        self.game_area = GameArea(fields, x_size, y_size, player_position)
        self.game_area_renderer = GameAreaRenderer(self.canvas, self.game_area)

    def create_game_area_from_file(self, file_name: str) -> None: # "-" je prazdne policko, "o" je objekt, "p" je hrac
        fields = []
        player_position = (0, 0) # defaultna hodnota
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for y, line in enumerate(lines):
                for x, symbol in enumerate(line.strip()):
                    has_object = symbol == "o"
                    fields.append(Field(has_object, x, y))
                    if (symbol == "p"):
                        player_position = (x, y)
        y_size = len(lines)
        x_size = len(lines[0].strip())

        self.game_area = GameArea(fields, x_size, y_size, player_position)
        self.game_area_renderer = GameAreaRenderer(self.canvas, self.game_area)

    def save_game_area_to_file(self, file_name: str):
        fields = [["-" for x in range(self.game_area.x_size)] for y in range(self.game_area.y_size)] # dvojrozmerne pole prazdnych policok
        for field in self.game_area.fields:
            if field.has_object:
                fields[field.y_position][field.x_position] = "o"
        fields[self.game_area.player_position[1]][self.game_area.player_position[0]] = "p"
        with open(file_name, 'w') as file:
            for line in fields:
                file.write("".join(map(str, line)) + "\n")

    def move_player(self, direction):
        #if self.game_area.is_valid_move(direction):
        self.game_area.move_player(direction)
        self.game_area_renderer.update_game_area()  # Call the rendering update method

    def on_key_press(self, event):
        if event.keysym == "Up":
            self.move_player("up")
        elif event.keysym == "Down":
            self.move_player("down")
        elif event.keysym == "Left":
            self.move_player("left")
        elif event.keysym == "Right":
            self.move_player("right")


class GameAreaRenderer:

    def __init__(self, canvas, game_area: GameArea) -> None:
        self.canvas = canvas
        self.game_area = game_area
        self.SOKOBAN_IMAGE = ImageTk.PhotoImage(Image.open("sokoban.png"))  # Store the image as an attribute
        self.CRATE_IMAGE = ImageTk.PhotoImage(Image.open("crate.png"))  # Store the image as an attribute

    def render_game_area(self):
        self.canvas.delete("all")
        FIELD_SIZE = 44
        self.canvas.config(width = self.game_area.x_size * FIELD_SIZE + 1, height = self.game_area.y_size * FIELD_SIZE + 1)
        for field in self.game_area.fields:
            y = field.x_position * FIELD_SIZE + 3
            x = field.y_position * FIELD_SIZE + 3
            if field.is_visited:
                color = "green"
            else:
                color = "yellow"
            self.canvas.create_rectangle(y, x, y + FIELD_SIZE, x + FIELD_SIZE, outline = "black", fill = color)
            if field.has_object:
                self.canvas.create_image(y, x, anchor = tk.NW, image = self.CRATE_IMAGE)
        self.canvas.create_image(self.game_area.player_position[1] * FIELD_SIZE + FIELD_SIZE / 2 + 3, \
                                 self.game_area.player_position[0] * FIELD_SIZE + FIELD_SIZE / 2 + 3, \
                                    anchor = tk.CENTER, image = self.SOKOBAN_IMAGE)

    def show_hamiltonian_path(self):
        pass

    def update_game_area(self):
        self.render_game_area()


#manager = GameAreaManager()
#manager.create_empty_game_area(3, 3)
#manager.game_area.get_field_by_position(1, 1).has_object = True
#print(HamiltonianPathSolver(manager.game_area).get_hamiltonian_path())
#print(HamiltonianPathSolver(manager.game_area).get_hamiltonian_path())
 
# Get the current directory of the active script
current_directory = os.path.dirname(os.path.abspath(__file__))
 
# List only .txt files in the current directory
txt_files = [f for f in os.listdir(current_directory) if f.endswith('.txt')]
 
# Print the list of .txt files
for txt_file in txt_files:
    print(txt_file)

#manager.create_empty_game_area(5, 2)
#manager.game_area.get_field_by_position(0, 1).has_object = True
#manager.save_game_area_to_file("map_test.txt")
