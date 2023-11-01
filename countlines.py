import os

def count_lines(filepath):
    """Count the non-empty lines in a Python file."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return sum(1 for line in lines if line.strip())

def count_py_lines(directory, exclude_dirs=None):
    """Recursively count all the lines of Python code in a given directory,
       and display the path/filename along with that file's line count."""
    if exclude_dirs is None:
        exclude_dirs = ['.git']
    total_lines = 0
    file_line_counts = {}
    for root, dirs, files in os.walk(directory):
        # print(root, directory, files)
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        # if '__pycache__' in root:
        #     continue
        # if 'venv' in root:
        #     continue
        # if '.git' in root:
        #     continue

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                line_count = count_lines(filepath)
                total_lines += line_count
                file_line_counts[filepath] = line_count
    return total_lines, file_line_counts

# directory = '/path/to/your/folder'

# get current folder
# current = os.getcwd()
directory = f'{os.getcwd()}'

total_lines, file_line_counts = count_py_lines(directory, exclude_dirs=['.git', 'venv', '__pycache__'])

# Display the line count for each file
for filepath, line_count in file_line_counts.items():
    print(f'{filepath}: {line_count} lines')

# Display the total lines of Python code
print(f'\nTotal lines of Python code: {total_lines}')