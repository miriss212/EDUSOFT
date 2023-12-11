from backend import Game
from frontend import WindowEditor
from PIL import Image, ImageTk
import time

class Command:
    # commandy ktore hrac pridava do postupnosti a cela postupnost sa potom skusti cez GameManager.execute_commands()

    def __init__(self) -> None:
        self.game: Game = None
        self.window_editor: WindowEditor = None

        self.game_manager = None

        # referencie na objekty sa nastavuju neskor objektom ktory pridava commandy do postupnosti

    def execute(self) -> None:
        raise NotImplementedError("This is abstract method!")
        # skonci ak ponorka narazi alebo ak nastane vyhra/prehra

    def _set_sonar_slider(self) -> None:
        submarine_level_position = self.game.submarine_position[0]
        self.window_editor.sonar_slider.set(submarine_level_position)
    
class GoShallowerCommand(Command):

    def __init__(self) -> None:
        
        super().__init__()
        command_img = Image.open("images/plus.png")
        command_img = command_img.resize((WindowEditor.COMMAND_SIZE - 5, WindowEditor.COMMAND_SIZE - 5), Image.LANCZOS)
        self.command_img = ImageTk.PhotoImage(command_img)
    
    def execute(self) -> None:

        time.sleep(0.5)
        self._set_sonar_slider()
        self.game_manager.redraw_canvas()
        self.window_editor.canvas.update()

        while self.game.go_shallower():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit cez self.game_manager.redraw_canvas()

            self._set_sonar_slider()
            time.sleep(0.5)
            self.game_manager.redraw_canvas()
            self.window_editor.canvas.update()

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoDeeperCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        command_img = Image.open("images/minus.png")
        command_img = command_img.resize((WindowEditor.COMMAND_SIZE - 5, WindowEditor.COMMAND_SIZE - 5), Image.LANCZOS)
        self.command_img = ImageTk.PhotoImage(command_img)
    
    def execute(self) -> None:

        time.sleep(0.5)
        self._set_sonar_slider()
        self.game_manager.redraw_canvas()
        self.window_editor.canvas.update()

        while self.game.go_deeper():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit cez self.game_manager.redraw_canvas()

            self._set_sonar_slider()
            time.sleep(0.5)
            self.game_manager.redraw_canvas()
            self.window_editor.canvas.update()

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoForwardCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        command_img = Image.open("images/arrow_up.png")
        command_img = command_img.resize((WindowEditor.COMMAND_SIZE - 5, WindowEditor.COMMAND_SIZE - 5), Image.LANCZOS)
        self.command_img = ImageTk.PhotoImage(command_img)
    
    def execute(self) -> None:

        time.sleep(0.5)
        self._set_sonar_slider()
        self.game_manager.redraw_canvas()
        self.window_editor.canvas.update()

        while self.game.go_forward():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit cez self.game_manager.redraw_canvas()

            self._set_sonar_slider()
            time.sleep(0.5)
            self.game_manager.redraw_canvas()
            self.window_editor.canvas.update()

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoBackCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        command_img = Image.open("images/arrow_down.png")
        command_img = command_img.resize((WindowEditor.COMMAND_SIZE - 5, WindowEditor.COMMAND_SIZE - 5), Image.LANCZOS)
        self.command_img = ImageTk.PhotoImage(command_img)
    
    def execute(self) -> None:

        time.sleep(0.5)
        self._set_sonar_slider()
        self.game_manager.redraw_canvas()
        self.window_editor.canvas.update()

        while self.game.go_back():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit cez self.game_manager.redraw_canvas()

            time.sleep(0.5)
            self.game_manager.redraw_canvas()
            self.window_editor.canvas.update()
            
            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoLeftCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        command_img = Image.open("images/arrow_left.png")
        command_img = command_img.resize((WindowEditor.COMMAND_SIZE - 5, WindowEditor.COMMAND_SIZE - 5), Image.LANCZOS)
        self.command_img = ImageTk.PhotoImage(command_img)

    def execute(self) -> None:

        time.sleep(0.5)
        self._set_sonar_slider()
        self.game_manager.redraw_canvas()
        self.window_editor.canvas.update()

        while self.game.go_left():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit cez self.game_manager.redraw_canvas()

            self._set_sonar_slider()
            time.sleep(0.5)
            self.game_manager.redraw_canvas()
            self.window_editor.canvas.update()

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break

class GoRightCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        command_img = Image.open("images/arrow_right.png")
        command_img = command_img.resize((WindowEditor.COMMAND_SIZE - 5, WindowEditor.COMMAND_SIZE - 5), Image.LANCZOS)
        self.command_img = ImageTk.PhotoImage(command_img)

    def execute(self) -> None:

        time.sleep(0.5)
        self._set_sonar_slider()
        self.game_manager.redraw_canvas()
        self.window_editor.canvas.update()

        while self.game.go_right():
            # TODO: pozastavit program aby animacia nebola moc rychla
            # TODO: vykreslit cez self.game_manager.redraw_canvas()

            self._set_sonar_slider()
            time.sleep(0.5)
            self.game_manager.redraw_canvas()
            self.window_editor.canvas.update()

            if self.game.check_lose():
                break
            
            if self.game.check_win():
                break