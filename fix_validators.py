import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replacements
    # cls: str, v: str -> None  => cls: type, v: Any -> Any
    new_content = re.sub(
        r'def (validate_[a-zA-Z0-9_]+)\(cls: str, v: str\) -> None:',
        r'def \1(cls: type, v: Any) -> Any:',
        content
    )
    
    # cls: str, v: str, info: str -> None => cls: type, v: Any, info: Any -> Any
    new_content = re.sub(
        r'def (validate_[a-zA-Z0-9_]+)\(cls: str, v: str, info: str\) -> None:',
        r'def \1(cls: type, v: Any, info: Any) -> Any:',
        new_content
    )

    # self: Self@... -> None => self -> Any
    new_content = re.sub(
        r'def ([a-zA-Z0-9_]+)\(self: Self@[a-zA-Z0-9_]+\) -> None:',
        r'def \1(self) -> Any:',
        new_content
    )
    
    # after validator: def name(self) -> None: => def name(self) -> Any:
    new_content = re.sub(
        r'def ([a-zA-Z0-9_]+)\(self\) -> None:(.*?)(?:return self)',
        r'def \1(self) -> Any:\2return self',
        new_content, flags=re.DOTALL
    )

    # Some might be def validate_...(cls: str, v: str) -> None
    # Let's just catch any (cls: str, v: str) -> None
    new_content = re.sub(
        r'\(cls: str, v: str\) -> None:',
        r'(cls: type, v: Any) -> Any:',
        new_content
    )

    new_content = re.sub(
        r'\(cls: str, v: str, info: str\) -> None:',
        r'(cls: type, v: Any, info: Any) -> Any:',
        new_content
    )

    # Check for -> None when there is a @model_validator(mode="after")
    # This might require a regex that looks back, but we can just blindly replace self -> None if we know it's a validator.
    # Actually, simpler: search for `@model_validator.*?\ndef [a-zA-Z_]+\(self\) -> None:`
    new_content = re.sub(
        r'(@model_validator[^>]*\n\s*def [a-zA-Z0-9_]+)\(self\) -> None:',
        r'\1(self) -> Any:',
        new_content
    )

    if content != new_content:
        # Check if 'from typing import Any' is present
        if 'from typing import ' in new_content and ' Any' not in new_content and 'Any,' not in new_content:
            new_content = re.sub(r'from typing import ', r'from typing import Any, ', new_content, count=1)
        elif 'typing' not in new_content:
            new_content = 'from typing import Any\n' + new_content
            
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, dirs, files in os.walk('argus'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))

