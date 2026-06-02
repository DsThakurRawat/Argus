import os

def remove_apache_headers(directory):
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Check if it has the Apache header
                            skip_mode = False
                            continue
                        if not skip_mode:
                            # Also filter out the Copyright header that usually precedes it
                            if 'Copyright' in line and line.startswith('#'):
                                continue
                            new_lines.append(line)
                    
                    with open(filepath, 'w') as f:
                        f.write('\n'.join(new_lines).lstrip())

remove_apache_headers('/home/divyansh-rawat/Argus/')
