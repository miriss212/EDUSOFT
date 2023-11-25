class Game:

    def __init__(self, map_file_path: str) -> None:
        
        self.map_file_path: str = map_file_path
        
        self.game_field: list[list[list[str]]] = None
        self.submarine_position: tuple[int, int, int] = None # [level, riadok, stlpec]
        self.submarina_oxygen: int = None
        self._generate_game_field()

    def _generate_game_field(self) -> None:
        with open(self.map_file_path, 'r') as map_file:
            map_file_content = map_file.read()

        for i in map_file_content.split('\n\n'):
            print(i)
            print()

    def restart_game(self) -> None:
        self._generate_game_field()

    def get_sonar_view(self, level: int) -> list[list[str]]:
        if 0 <= level < len(self.game_field):
            return self.game_field[level]
        
    def check_win(self) -> bool:
        return self.game_field[self.submarine_position[0]][self.submarine_position[1]][self.submarine_position[2]] == "P"
    

Game("Edusoft_2/test_map.txt")