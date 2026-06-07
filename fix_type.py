import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content.replace("cls: type,", "cls: Any,")

    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, dirs, files in os.walk('argus'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))

