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
    # TODO: trieda pre vykreslovanie vsetkeho v okne
    pass

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

# test
map_editor = WindowEditor()
game_manager = GameManager(map_editor)

game_manager.new_game("Edusoft_2/test_map.txt")