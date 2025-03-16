commands = {
    'create_venv': 'python -m venv ',
    'install_module': '-m pip install ',
    'activate_venv': '\\Scripts\\python.exe',
    'create_file': 'powershell -Command New-Item -Path file-path\\file-name -ItemType File',
    'create_dir': 'powershell -Command mkdir name',
    'ls': 'powershell -Command ls',
    'cd': 'powershell -Command cd dir'
}


commands_dict_linux = {
    'create_venv': 'python3 -m venv ',
    'install_module': '-m pip3 install ',
    'activate_venv': '/bin/activate',
    'create_file': 'touch file-path/file-name',
    'create_dir': 'mkdir name',
    'ls': 'ls',
    'cd': 'cd dir'
}
