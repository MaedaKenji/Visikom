import os

def remove_comments(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    with open(output_file_path, 'w') as file:
        for line in lines:
            stripped_line = line.split('#')[0].rstrip()
            if stripped_line:  # Write only non-empty lines
                file.write(stripped_line + '\n')

# Example usage
dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(dir, 'main.py')  # Replace with the path to your input file
output_file = 'main_no_comments.py'  # Replace with the desired output file name
remove_comments(input_file, output_file)