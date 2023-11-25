class Game:

    def __init__(self, map_file_path: str) -> None:
        
        self.map_file_path: str = map_file_path
        
        self.game_field: list[list[list[str]]] = None
        self.submarine_position: tuple[int, int, int] = None # [level, riadok, stlpec]
        self.submarine_oxygen: int = None
        self._generate_game_field()

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


    def restart_game(self) -> None:
        self._generate_game_field()

    def get_sonar_view(self, level: int) -> list[list[str]]:
        if 0 <= level < len(self.game_field):
            return self.game_field[level]
        
    def check_win(self) -> bool:
        return self.game_field[self.submarine_position[0]][self.submarine_position[1]][self.submarine_position[2]] == "P"
    
    def check_lose(self) -> bool:
        return self.submarine_oxygen == 0
    
    def go_shallower(self) -> None:
        pass

    def go_deeper(self) -> None:
        pass

    def go_up(self) -> None:
        pass

    def go_down(self) -> None:
        pass

    def go_left(self) -> None:
        pass

    def go_right(self) -> None:
        pass
    
# game = Game("Edusoft_2/test_map.txt")
# print(game.get_sonar_view(1))
# print(game.submarine_position)