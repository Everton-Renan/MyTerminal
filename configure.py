import json
import sys

with open('data.json', 'w', encoding='utf8') as file:
    path = {'path': sys.argv[0]}
    json.dump(path, file)

import main
