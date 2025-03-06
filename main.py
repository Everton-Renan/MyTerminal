import argparse
import json
import os
import subprocess
from pathlib import Path
from tkinter.filedialog import askdirectory

from myterminal.commands_dict import commands_dict

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

    def execute_command(self, command: str | list) -> bool:
        try:
            if os.path.exists(self.get_path()):
                if isinstance(command, str):
                    command_to_run = UnpackingCommands(command).unpacking()
                elif isinstance(command, list):
                    unpacked_command = list()
                    command_to_run = list()

                    for i in command:
                        unpacked_command = UnpackingCommands(i).unpacking()
                        for c in unpacked_command:
                            command_to_run.append(c)

                subprocess.run(command_to_run, cwd=self.get_path(),
                               capture_output=True,
                               text=True, check=True)
            else:
                raise FileNotFoundError('Folder not found.')

        except FileNotFoundError as error:
            self.show_error_message(error)
            return False

        except subprocess.CalledProcessError as error:
            if error.stderr:
                self.show_error_message(error.stderr)
            return False

        except PermissionError as error:
            self.show_error_message(error)
            return False

        return True

    def show_error_message(self, error: Exception | str) -> None:
        print(
            f'{ERROR_COLOR}MyTerminal (output): {error}{RESET_COLOR}')

    def show_message(self, text: str) -> None:
        print(
            f'{OUTPUT_COLOR}MyTerminal (output): {text} {RESET_COLOR}')

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
            create_parser.add_argument('-i', '--install', nargs='+',
                                       help='Enter the name of the modules'
                                       ' you want to install in the virtual'
                                       ' environment.')

            if manager_parser.parse_args(commands):
                args = manager_parser.parse_args(commands)
                if args.type == 'venv':
                    command = commands_dict['create_venv'] + args.name
                    if not self.execute_command(command):
                        return False

                    self.show_message(
                        'Virtual environment created successfully.')

                    if args.install:
                        installed_modules = []
                        for module in args.install:
                            name = '\\' + args.name
                            python_path = self.get_path() + name + \
                                commands_dict['activate_venv']
                            command = commands_dict['install_module'] + \
                                module

                            if not self.execute_command(
                                [python_path, command]
                            ):
                                self.show_error_message(
                                    'An error occurred while '
                                    f'installing the module {module}.')

                                continue

                            installed_modules.append(module)
                        self.show_message(
                            f'The modules {installed_modules} have been '
                            'installed successfully.')
                        return True
                    else:
                        return True

        elif commands[0] == 'install':
            install_parser = subparsers.add_parser(
                'install', help='Enter the name of the module you want '
                'to install.')

            install_parser.add_argument(
                'name', help='Enter the name of the virtual environment.')

            install_parser.add_argument('install', nargs='+', help='Enter the '
                                        'name of the module you want '
                                        'to install.')

            if manager_parser.parse_args(commands):
                args = manager_parser.parse_args(commands)

                if args.install == ['']:
                    self.show_error_message('No modules sent.')
                    return False

                installed_modules = []
                for module in args.install:
                    name = '\\' + args.name
                    python_path = self.get_path() + name + \
                        commands_dict['activate_venv']

                    if not os.path.exists(python_path):
                        self.show_error_message('Virtual environment '
                                                f'({args.name}) not found.')
                        return False

                    command = commands_dict['install_module'] + \
                        module

                    if not self.execute_command([python_path, command]):
                        self.show_error_message(
                            'An error occurred while '
                            f'installing the module {module}.'
                        )

                        continue

                    installed_modules.append(module)
                self.show_message(
                    f'The modules {installed_modules} have been '
                    'installed successfully.')
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
