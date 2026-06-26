from pathlib import Path

HEADER = """# Copyright 2026 Divyansh Rawat
#

"""

EXTENSIONS = {".py", ".sh"}


def update_headers():
    root = Path(".")
    count = 0
    for path in root.rglob("*"):
        if path.suffix in EXTENSIONS and "venv" not in str(path) and ".git" not in str(path):
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()

                # Skip if header already exists
                if "Copyright 2026 Divyansh Rawat" in content:
                    continue

                # Remove old headers if they exist (simple check for "Copyright")
                lines = content.splitlines()
                if lines and (
                    "Copyright" in lines[0] or "License" in lines[0] or lines[0].startswith("#!")
                ):
                    # If it's a shebang, keep it and insert header after
                    if lines[0].startswith("#!"):
                        new_content = lines[0] + "\n\n" + HEADER + "\n".join(lines[1:])
                    else:
                        # Find where old block ends or just prepend
                        new_content = HEADER + content
                else:
                    new_content = HEADER + content

                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1
                print(f"Updated: {path}")
            except Exception as e:
                print(f"Error updating {path}: {e}")

    print(f"\n✅ Successfully updated {count} files.")


if __name__ == "__main__":
    update_headers()
