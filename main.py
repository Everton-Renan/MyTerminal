import argparse
import json
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
        return self._command.split(' ')


class Terminal:
    def set_path(self, path: str | Path) -> bool:
        if not os.path.exists(path):
            try:
                raise FileNotFoundError('Folder not Found.')
            except FileNotFoundError as error:
                self.show_error_message(error)
                return False

        if path is not None:
            with open('data.json', 'w', encoding='utf8') as file:
                info = {'path': str(path)}
                json.dump(info, file, ensure_ascii=False, indent=2)

            return True
        else:
            return False

    def get_path(self) -> str:
        with open('data.json', 'r', encoding='utf8') as file:
            info = json.load(file)
            return info['path']

    def execute_command(self, command: str) -> bool:
        try:
            if os.path.exists(self.get_path()):
                subprocess.run(command, cwd=self.get_path(),
                               capture_output=True,
                               text=True, check=True)
            else:
                raise FileNotFoundError('Folder not found.')

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

        manager_parser = argparse.ArgumentParser(
            'Manages the creation and removal of files and '
            'virtual environments')

        subparsers = manager_parser.add_subparsers(
            dest='action', required=True, description='Choose an action.')

        select_parser = argparse.ArgumentParser('Select folder.')
        select_parser.add_argument('select_folder', help='Select folder.')
        select_parser.add_argument(
            '-p', '--path', nargs='?', help='Enter the path to the folder.')

        if commands[0] == 'select_folder':
            select_args = select_parser.parse_args(commands)
            if not select_args.path:
                ask = askdirectory()
                path = Path(ask)
                self.set_path(path)
                return True
            else:
                path = Path(select_args.path)
                if not self.set_path(path):
                    return False

                return True

        elif commands[0] == 'create':
            create_parser = subparsers.add_parser('create', help='Create.')
            create_parser.add_argument('type', help='Choose the type.')
            create_parser.add_argument(
                'name', nargs='?', help='Choose the name', default='venv')

            if manager_parser.parse_args(commands):
                args = manager_parser.parse_args(commands)
                if args.type == 'venv':
                    command = create_commands['create_venv'] + args.name
                    self.execute_command(command)
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
    user_input = input(
        f'{INPUT_COLOR}MyTerminal (input): {RESET_COLOR}').lower()
    if user_input == 'exit':
        print(f'{OUTPUT_COLOR}MyTerminal (output): Bye!{RESET_COLOR}')
        break
    unpack = UnpackingCommands(user_input)
    unpacked_commands = unpack.unpacking()

    run_commands = RunCommands(unpacked_commands)
    print(run_commands.run_commands())
