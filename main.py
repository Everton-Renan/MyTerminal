import os
import subprocess

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
    def execute_command(self, command: str) -> bool:

        try:
            if not os.path.exists(self._path):
                raise FileNotFoundError(
                    f'The folder {self._path} was not found.')

        except FileNotFoundError as error:
            self.show_error_message(error)
            return False

        try:
            subprocess.run(command, capture_output=True, text=True, check=True)

        except subprocess.CalledProcessError as error:
            self.show_error_message(error)
            return False

        except PermissionError as error:
            self.show_error_message(error)
            return False

        except FileNotFoundError as error:
            self.show_error_message(error)
            return False

        return True

    def show_error_message(self, error: Exception):
        print(f'{ERROR_COLOR}MyTerminal (output): {error} {RESET_COLOR}')

    def run(self, commands: list[str]) -> bool:
        if 'create' in commands:
            if 'venv' in commands:
                command = create_commands['create_venv'] + commands[2] + ' '
                if '-p' in commands:
                    self._path = commands[4]
                    command = create_commands['create_venv'] + \
                        self._path + f'/{commands[2]} '

        if self.execute_command(command):
            return True
        return False


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
