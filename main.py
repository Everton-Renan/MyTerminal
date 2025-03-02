import argparse
import os
import subprocess
from pathlib import Path
from tkinter.filedialog import askdirectory

from myterminal.commands_dict import create_commands

INPUT_COLOR = '\033[32m'
ERROR_COLOR = '\033[31m'
RESET_COLOR = '\033[0m'
OUTPUT_COLOR = '\033[34m'


class UnpackingCommands:
    def __init__(self, command: str) -> None:
        self._command = command

    def unpacking(self) -> list[str]:
        return command.split(' ')


class Terminal:
    def set_path(self, path) -> bool:
        self._path = path
        return True

    def get_path(self) -> str | None:
        return self._path

    def execute_command(self, command: str) -> bool:
        try:
            if os.path.exists(self._path):
                subprocess.run(command, cwd=self.get_path(),
                               capture_output=True,
                               text=True, check=True)
            else:
                raise FileNotFoundError

        except FileNotFoundError as error:
            self.show_error_message(error)
            return False

        except subprocess.CalledProcessError as error:
            self.show_error_message(error)
            return False

        except PermissionError as error:
            self.show_error_message(error)
            return False

        return True

    def show_error_message(self, error: Exception):
        print(f'{ERROR_COLOR}MyTerminal (output): {error} {RESET_COLOR}')

    def run(self, commands: list[str]) -> bool:
        select_parser = argparse.ArgumentParser('Select folder.')
        select_parser.add_argument('select_folder', help='Select folder.')

        if select_parser.parse_args(commands):
            ask = askdirectory()
            path = Path(ask)
            self.set_path(path)
            return True


class RunCommands:
    def __init__(self, commands: list[str]) -> None:
        self._commands = commands
        self._terminal = Terminal()

    def run_commands(self) -> bool:
        if self._terminal.run(self._commands):
            return True
        return False


while True:
    command = input(f'{INPUT_COLOR}MyTerminal (input): {RESET_COLOR}').lower()
    if command == 'exit':
        print(f'{OUTPUT_COLOR}MyTerminal (output): Bye!{RESET_COLOR}')
        break
    unpack = UnpackingCommands(command)
    unpacked_commands = unpack.unpacking()

    run_commands = RunCommands(unpacked_commands)
    print(run_commands.run_commands())
