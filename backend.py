import copy

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
        self.get_field_by_position(player_position[0], player_position[1]).is_visited = True

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
        valid_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)] # hore, dole, doprava, dolava
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

    def __init__(self) -> None:
        self.game_area = None

    def create_empty_game_area(self, x_size: int, y_size: int) -> None:
        fields = []
        player_position = (0 ,0) # (x, y)
        for y in range(y_size):
            for x in range(x_size):
                fields.append(Field(False, x, y))
        self.game_area = GameArea(fields, x_size, y_size, player_position)

    def create_game_area_from_file(self, file_name: str) -> None:
        pass

manager = GameAreaManager()
manager.create_empty_game_area(3, 3)
manager.game_area.get_field_by_position(1, 1).has_object = True
print(HamiltonianPathSolver(manager.game_area).get_hamiltonian_path())