command = input('MyTerminal (input): ')


class UnpackingCommands:
    def __init__(self, command: str) -> None:
        self._command = command

    def unpacking(self) -> list[str]:
        return command.split(' ')
