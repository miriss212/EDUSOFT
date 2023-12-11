class Game:
    # trieda pre hraciu plochu

    BUBBLE_VALUE: int = 5

    def __init__(self, map_file_path: str) -> None:
        self.map_file_path: str = map_file_path
        
        self.game_field: list[list[list[str]]] = None
        self.submarine_position: tuple[int, int, int] = None # [level, row, column]
        self.submarine_oxygen: int = None
        self.submarine_direction: str = "right"

        self._generate_game_field()
    
    def get_map_depth(self) -> int:
        return len(self.game_field)

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
        return self._move_to(self.submarine_position[0] + 1, self.submarine_position[1], self.submarine_position[2])

    def go_deeper(self) -> bool:
        return self._move_to(self.submarine_position[0] - 1, self.submarine_position[1], self.submarine_position[2])

    def go_forward(self) -> bool:
        self.submarine_direction = "up"
        return self._move_to(self.submarine_position[0], self.submarine_position[1] - 1, self.submarine_position[2])

    def go_back(self) -> bool:
        self.submarine_direction = "down"
        return self._move_to(self.submarine_position[0], self.submarine_position[1] + 1, self.submarine_position[2])

    def go_left(self) -> bool:
        self.submarine_direction = "left"
        return self._move_to(self.submarine_position[0], self.submarine_position[1], self.submarine_position[2] - 1)

    def go_right(self) -> bool:
        self.submarine_direction = "right"
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

            # vymazanie bublin
            self.game_field[level][row][column] = "V"

        self.submarine_position = (level, row, column)
        self.submarine_oxygen -= 1
        return True