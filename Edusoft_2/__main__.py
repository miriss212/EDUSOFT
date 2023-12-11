from frontend import WindowEditor
from backend import Game
from commands import *
from tkinter import filedialog
from tkinter import messagebox

class GameManager:
    # trieda pre riadenie celej hry (aplikacie)

    def __init__(self, map_editor: WindowEditor, game: Game) -> None:
        self.commands: list[Command] = []
        self.actual_command_index: int = None

        self.window_editor: WindowEditor = map_editor
        self.game: Game = game

        self._set_button_functions()
        self.redraw_canvas()
        self._bind_key_events()
        self.window_editor.master.mainloop()

    def redraw_canvas(self) -> None:
        sonar_value = int(self.window_editor.sonar_slider.get())
        self.window_editor.redraw_canvas(self.game.get_sonar_view(int(sonar_value)), self.game.submarine_position, self.game.submarine_oxygen, self.commands, self.actual_command_index, self.game.submarine_direction)

    def add_command(self, command: Command) -> None:

        if len(self.commands) >= 10:
            return
        
        # tu sa nastavia referencie na objekty
        command.game = self.game
        command.window_editor = self.window_editor
        command.game_manager = self

        self.commands.append(command)

        self.redraw_canvas()

    def remove_last_command(self) -> None:
        if len(self.commands) > 0:
            self.commands.pop()

        self.redraw_canvas()

    def execute_commands(self) -> None:

        self._unbind_key_events()

        for index, command in enumerate(self.commands):
            self.actual_command_index = index
            command.execute()

            if command.game.check_win():
                messagebox.showinfo("Výhra", "Výborne! Ponorka našla poklad :)")
                self.restart_game()
                return
            
            if command.game.check_lose():
                messagebox.showinfo("Prehra", "Ponorke došiel vzduch :( Skús to znova!")
                self.restart_game()
                return
        
        # TODO: ponorka ostala na polceste (restart hry?)
        messagebox.showinfo("Prehra", "Ponorka nenašla poklad :( Skús to znova!")
        self.restart_game()

    # nova hra ked si hrac vybere nejaku mapu
    def new_game(self) -> None:
        # Configure options for the dialog
        options = {
            'defaultextension': '.txt',  # Default file extension
            'filetypes': [("Text Files", "*.txt")],  # List of file types
            'initialdir': 'maps'
        }
 
        map_file_path = filedialog.askopenfilename(**options)

        self.window_editor.master.destroy()
        self.window_editor = WindowEditor()
        self._set_button_functions()

        self.game = Game(map_file_path)

        self.commands = []
        self.actual_command_index = None

        self._bind_key_events()
        self.redraw_canvas()

        self.window_editor.master.mainloop()

    def restart_game(self) -> None:
        map_file_path = self.game.map_file_path

        self.window_editor.master.destroy()
        self.window_editor = WindowEditor()
        self._set_button_functions()

        self.game = Game(map_file_path)

        self.commands = []
        self.actual_command_index = None

        self._bind_key_events()
        self.redraw_canvas()

        self.window_editor.master.mainloop()

    def _set_button_functions(self) -> None:
        self.window_editor.set_new_game_button(self.new_game)
        self.window_editor.set_restart_game_button(self.restart_game)
        self.window_editor.set_execute_commands_button(self.execute_commands)
        self.window_editor.set_sonar_slider(0, self.game.get_map_depth() - 1, lambda value: self.redraw_canvas())

    def _bind_key_events(self) -> None:
        self.window_editor.master.bind("<Up>", lambda event: self.add_command(GoForwardCommand()))
        self.window_editor.master.bind("<Down>", lambda event: self.add_command(GoBackCommand()))
        self.window_editor.master.bind("<Left>", lambda event: self.add_command(GoLeftCommand()))
        self.window_editor.master.bind("<Right>", lambda event: self.add_command(GoRightCommand()))
        self.window_editor.master.bind("<H>", lambda event: self.add_command(GoDeeperCommand()))
        self.window_editor.master.bind("<h>", lambda event: self.add_command(GoDeeperCommand()))
        self.window_editor.master.bind("<P>", lambda event: self.add_command(GoShallowerCommand()))
        self.window_editor.master.bind("<p>", lambda event: self.add_command(GoShallowerCommand()))
        self.window_editor.master.bind("<BackSpace>", lambda event: self.remove_last_command())

    def _unbind_key_events(self) -> None:
        self.window_editor.master.unbind("<Up>")
        self.window_editor.master.unbind("<Down>")
        self.window_editor.master.unbind("<Left>")
        self.window_editor.master.unbind("<Right>")
        self.window_editor.master.unbind("<H>")
        self.window_editor.master.unbind("<h>")
        self.window_editor.master.unbind("<P>")
        self.window_editor.master.unbind("<p>")
        self.window_editor.master.unbind("<BackSpace>")

map_editor = WindowEditor()
game = Game("maps/mapa_1.txt")
game_manager = GameManager(map_editor, game)