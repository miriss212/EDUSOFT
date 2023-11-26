import backend

class MapEditor:
    # TODO: trieda pre vykreslovanie vsetkeho
    pass

class Command:
    
    def __init__(self) -> None:
        self.game: backend.Game = None
        self.map_editor: MapEditor = None

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

    def __init__(self, map_editor: MapEditor) -> None:
        self.map_editor: MapEditor = map_editor
        self.game: backend.Game = None

        self.commands: list[Command] = []
        # TODO: vykreslit okno s prazdnym canvasom lebo self.game == None (hra sa vybere zo suboru)

    def add_command(self, command: Command) -> None:
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

    def new_game(self, map_file_path: str) -> None:
        self.game = backend.Game(map_file_path)

        self.commands = []
        # TODO: nanovo vykreslit hru

    def restart_game(self) -> None:
        if self.game is not None:
            self.game.restart_game()

        self.commands = []
        # TODO: nanovo vykreslit hru

map_editor = MapEditor()
game_manager = GameManager(map_editor)
game_manager.new_game("Edusoft_2/test_map.txt")